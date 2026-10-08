import XCTest

/// The core walk: for every artifact in the capture plan, launch once, confirm
/// the page count, then capture every requested page/slide deterministically.
///
/// Navigation is done through the app's own Prev/Next buttons, gated on the
/// exact "Page N of M" indicator before every capture, so a missed tap can
/// never silently capture the wrong page (single launch per artifact instead of
/// one launch per page).
final class ArtifactWalkTests: XCTestCase {

    private struct WalkCounts {
        var launchCount = 0
        var artifactLoads = 0
        var captureCount = 0
    }

    func testWalkAllArtifacts() throws {
        let support = try TestSupport.load()
        try support.prepareOutput()

        var launchCount = 0
        var artifactLoads = 0
        var captureCount = 0

        for item in support.capturePlanItems() {
            guard let artifact = support.manifest.artifact(byId: item.artifactId) else {
                XCTFail("artifact not found in manifest: \(item.artifactId)")
                continue
            }
            let pages = item.pages ?? Array(1...artifact.expectedPages)
            let counts = try captureArtifact(artifact: artifact, pages: pages, support: support)
            launchCount += counts.launchCount
            artifactLoads += counts.artifactLoads
            captureCount += counts.captureCount
        }

        try support.writeHarnessStats(
            launchCount: launchCount,
            artifactLoads: artifactLoads,
            captureCount: captureCount
        )
    }

    private func captureArtifact(artifact: Artifact, pages: [Int], support: TestSupport) throws -> WalkCounts {
        var counts = WalkCounts()
        let sorted = pages.sorted()
        guard let first = sorted.first else { return counts }

        let app = XCUIApplication()
        app.launchArguments = [
            "-artifactPath", support.absoluteSource(artifact.sourcePath).path,
            "-viewMode", artifact.viewMode,
            "-orientation", artifact.orientation,
            "-page", String(first),
        ]
        app.launch()
        counts.launchCount += 1
        counts.artifactLoads += 1

        // Rotate the simulator to the artifact's requested orientation.
        setDeviceOrientation(artifact.orientation)

        let loadError = app.staticTexts["loadError"]
        if loadError.waitForExistence(timeout: 10) {
            XCTFail("load error for \(artifact.artifactId): \(loadError.label)")
            app.terminate()
            return counts
        }

        let indicator = app.staticTexts["pageIndicator"]
        XCTAssertTrue(
            indicator.waitForExistence(timeout: 15),
            "pageIndicator missing for \(artifact.artifactId)"
        )

        var current = first
        for page in sorted {
            // Navigate deterministically to `page`, verifying the indicator on
            // every step so navigation is never assumed.
            let step = page > current ? 1 : -1
            var cursor = current
            while cursor != page {
                let button = step > 0 ? app.buttons["nextButton"] : app.buttons["prevButton"]
                button.tap()
                cursor += step
                guard waitForLabel(indicator, "Page \(cursor) of \(artifact.expectedPages)", timeout: 20) else {
                    XCTFail(
                        "navigation to page \(cursor) failed for \(artifact.artifactId) " +
                        "(indicator reads '\(indicator.label)')"
                    )
                    app.terminate()
                    return counts
                }
            }

            // Confirm the exact target page before capture (covers the first page too).
            guard waitForLabel(indicator, "Page \(page) of \(artifact.expectedPages)", timeout: 20) else {
                XCTFail(
                    "page count / page mismatch for \(artifact.artifactId) page \(page): " +
                    "expected \(artifact.expectedPages) pages, indicator reads '\(indicator.label)'"
                )
                app.terminate()
                return counts
            }

            let shot = app.screenshot()
            let png = shot.pngRepresentation
            let url = support.screenshotURL(artifact: artifact, page: page)
            try png.write(to: url)

            let record = CaptureRecord(
                artifactId: artifact.artifactId,
                artifactType: artifact.artifactType,
                artifactSHA256: artifact.artifactSHA256,
                pdfPage: page,
                deviceModel: support.runConfig.deviceModel,
                osVersion: support.runConfig.osVersion,
                viewportPixels: TestSupport.pixelSize(ofPNG: png)
                    ?? ["width": 0, "height": 0],
                orientation: artifact.orientation,
                viewMode: artifact.viewMode,
                zoomScale: Self.parseScale(app.staticTexts["modeLabel"].label),
                screenshotSHA256: TestSupport.sha256(png),
                screenshotPath: url.path,
                runId: support.runConfig.runId,
                buildId: support.runConfig.buildId
            )
            try support.appendRecord(record)
            counts.captureCount += 1
            current = page
        }

        app.terminate()
        return counts
    }

    private func waitForLabel(_ element: XCUIElement, _ label: String, timeout: TimeInterval) -> Bool {
        let predicate = NSPredicate(format: "label == %@", label)
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
        return XCTWaiter().wait(for: [expectation], timeout: timeout) == .completed
    }

    private func setDeviceOrientation(_ orientation: String) {
        let device = XCUIDevice.shared
        switch orientation {
        case "landscape":
            device.orientation = .landscapeLeft
        case "portrait":
            device.orientation = .portrait
        default:
            device.orientation = .portrait
        }
    }

    private static func parseScale(_ label: String) -> Double? {
        guard let range = label.range(of: #"x[0-9.]+"#, options: .regularExpression) else {
            return nil
        }
        return Double(label[range].dropFirst())
    }
}
