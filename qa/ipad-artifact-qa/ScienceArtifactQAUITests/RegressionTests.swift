import CryptoKit
import XCTest

/// Deterministic regression tests. These prove screenshot capture mechanics,
/// not aesthetic judgement. Aesthetic findings are candidates for the blind
/// reviewer, never release verdicts here.
final class RegressionTests: XCTestCase {

    private var support: TestSupport {
        get throws { try TestSupport.load() }
    }

    private func repoRoot() throws -> URL {
        try support.repoRoot
    }

    private func fixture(_ name: String) throws -> URL {
        try repoRoot()
            .appendingPathComponent("qa/temp/ipad-artifact-qa/fixtures")
            .appendingPathComponent(name)
    }

    // MARK: - Launch-time failures

    func testMissingPDFFails() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-artifactPath", "/nonexistent/does-not-exist.pdf"]
        app.launch()
        let loadError = app.staticTexts["loadError"]
        XCTAssertTrue(loadError.waitForExistence(timeout: 10), "expected a load error for a missing PDF")
        XCTAssertTrue(loadError.label.contains("not found"), "unexpected error text: \(loadError.label)")
        app.terminate()
    }

    func testMalformedPDFFails() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-artifactPath", try fixture("malformed.pdf").path]
        app.launch()
        let loadError = app.staticTexts["loadError"]
        XCTAssertTrue(loadError.waitForExistence(timeout: 10), "expected a load error for a malformed PDF")
        app.terminate()
    }

    func testValidPDFReportsPageCount() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-artifactPath", try fixture("fixture-2page.pdf").path]
        app.launch()
        let indicator = app.staticTexts["pageIndicator"]
        XCTAssertTrue(indicator.waitForExistence(timeout: 10))
        let predicate = NSPredicate(format: "label == %@", "Page 1 of 2")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: indicator)
        XCTAssertEqual(XCTWaiter().wait(for: [expectation], timeout: 10), .completed)
        app.terminate()
    }

    // MARK: - Manifest integrity

    func testManifestHashesMatchFilesOnDisk() throws {
        let s = try support
        for artifact in s.manifest.artifacts {
            let data = try Data(contentsOf: s.absoluteSource(artifact.sourcePath))
            let actual = TestSupport.sha256(data)
            XCTAssertEqual(
                actual,
                artifact.artifactSHA256,
                "hash mismatch for \(artifact.artifactId): manifest \(artifact.artifactSHA256) vs file \(actual)"
            )
        }
    }

    func testScreenshotFilenamesAreUniquePerArtifact() throws {
        let s = try support
        for artifact in s.manifest.artifacts {
            var seen = Set<String>()
            for page in 1...artifact.expectedPages {
                let name = s.screenshotName(artifact: artifact, page: page)
                XCTAssertFalse(seen.contains(name), "duplicate screenshot filename \(name)")
                seen.insert(name)
            }
        }
    }

    /// Deterministic proof that orientation was applied on every capture:
    /// portrait artifacts produce tall images, landscape artifacts wide images.
    func testCapturedOrientationsMatchManifest() throws {
        let s = try support
        let lines = try s.readCaptureRecords()
        try XCTSkipIf(lines.isEmpty, "no capture records yet — run the artifact walk first")
        for rec in lines {
            let w = rec.viewportPixels["width"] ?? 0
            let h = rec.viewportPixels["height"] ?? 0
            switch rec.orientation {
            case "landscape":
                XCTAssertGreaterThan(w, h, "\(rec.artifactId) p\(rec.pdfPage): landscape but viewport \(w)x\(h)")
            case "portrait":
                XCTAssertGreaterThan(h, w, "\(rec.artifactId) p\(rec.pdfPage): portrait but viewport \(w)x\(h)")
            default:
                break
            }
        }
    }
}
