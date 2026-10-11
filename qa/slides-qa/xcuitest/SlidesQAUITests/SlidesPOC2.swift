import XCTest

/// POC #2: enter present mode, capture slide 1, advance, capture slide 2,
/// and dump the present-mode accessibility tree to discover navigation controls.
final class SlidesPOC2: XCTestCase {

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

    func testEnterPresentModeAndAdvance() throws {
        let slides = XCUIApplication(bundleIdentifier: "com.google.Slides")
        slides.activate()
        XCTAssertTrue(slides.wait(for: .runningForeground, timeout: 30))

        // Enter presentation mode.
        let startButton = slides.buttons["Start presentation"]
        if startButton.waitForExistence(timeout: 15) {
            startButton.tap()
        } else {
            // Fallback: the button may be labelled differently.
            print("=== NO 'Start presentation' button; dumping tree ===")
            print(slides.debugDescription)
            throw XCTSkip("Start presentation button not found")
        }

        // Give present mode a moment to load.
        sleep(3)

        // Dump present-mode tree.
        let tree = slides.debugDescription
        print("=== PRESENT MODE TREE BEGIN ===")
        print(tree)
        print("=== PRESENT MODE TREE END ===")
        add(XCTAttachment(string: tree).then { $0.name = "present-tree.txt"; $0.lifetime = .keepAlways })

        // Capture slide 1 (present mode).
        snapshot("slide-01.png")

        // Attempt to advance: look for a "Next slide" button; else swipe left.
        let next = slides.buttons["Next slide"]
        if next.waitForExistence(timeout: 3) {
            next.tap()
        } else {
            slides.swipeLeft()
        }
        sleep(2)

        // Capture slide 2.
        snapshot("slide-02.png")

        // Record the accessible slide indicator if present.
        print("=== PRESENT COUNTS: buttons=\(slides.buttons.count) staticTexts=\(slides.staticTexts.count) ===")
    }
}

private extension XCTAttachment {
    func then(_ block: (XCTAttachment) -> Void) -> XCTAttachment {
        block(self)
        return self
    }
}
