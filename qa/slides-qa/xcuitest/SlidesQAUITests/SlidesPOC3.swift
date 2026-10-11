import XCTest

/// POC #3: correct present-mode entry flow (Start presentation → Present on
/// this device), then discover present-mode navigation controls and capture
/// two distinct slides.
final class SlidesPOC3: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    private func snapshot(_ name: String) {
        let shot = XCUIScreen.main.screenshot()
        let att = XCTAttachment(screenshot: shot)
        att.name = name
        att.lifetime = .keepAlways
        add(att)
    }

    private func dumpTree(_ name: String, _ app: XCUIApplication) {
        let tree = app.debugDescription
        print("=== \(name) TREE BEGIN ===")
        print(tree)
        print("=== \(name) TREE END ===")
        let att = XCTAttachment(string: tree)
        att.name = name
        att.lifetime = .keepAlways
        add(att)
    }

    func testCorrectPresentFlow() throws {
        let slides = XCUIApplication(bundleIdentifier: "com.google.Slides")
        slides.activate()
        XCTAssertTrue(slides.wait(for: .runningForeground, timeout: 30))

        // 1. Open the presentation-options popover.
        let start = slides.buttons["Start presentation"]
        XCTAssertTrue(start.waitForExistence(timeout: 15), "Start presentation button missing")
        start.tap()
        sleep(1)

        // 2. Choose "Present on this device".
        let onDevice = slides.cells["Present on this device"]
            .firstMatch
        // The cell may be exposed as a static text inside a cell; try both.
        if !onDevice.waitForExistence(timeout: 5) {
            let label = slides.staticTexts["Present on this device"]
            XCTAssertTrue(label.waitForExistence(timeout: 5), "Present on this device option missing")
            label.tap()
        } else {
            onDevice.tap()
        }
        sleep(4)  // allow present mode to fully enter

        // 3. Dump present-mode tree to discover navigation controls.
        dumpTree("present-mode-tree.txt", slides)

        // 4. Capture slide 1 in full present mode.
        snapshot("slide-01.png")

        // 5. Attempt advance. Prefer an explicit control, else swipe.
        let next = slides.buttons["Next slide"]
        if next.waitForExistence(timeout: 3) {
            next.tap()
        } else {
            // Swipe on the main slide canvas (full-screen area).
            slides.coordinate(withNormalizedOffset: CGVector(dx: 0.8, dy: 0.5))
                .press(forDuration: 0.05, thenDragTo: slides.coordinate(withNormalizedOffset: CGVector(dx: 0.2, dy: 0.5)))
        }
        sleep(2)

        // 6. Capture slide 2.
        snapshot("slide-02.png")

        // 7. Dump tree again to find any slide-position indicator.
        dumpTree("after-advance-tree.txt", slides)
    }
}
