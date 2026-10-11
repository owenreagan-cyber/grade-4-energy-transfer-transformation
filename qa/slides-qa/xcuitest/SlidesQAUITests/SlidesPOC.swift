import XCTest

/// Bounded proof of concept: attach to the native Google Slides app (already
/// opened to the Chapter 1 presentation via deep link), dump the accessibility
/// hierarchy, and capture the current slide.
final class SlidesPOC: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testAttachAndDumpHierarchy() throws {
        let slides = XCUIApplication(bundleIdentifier: "com.google.Slides")
        slides.activate()

        let foreground = slides.wait(for: .runningForeground, timeout: 30)
        XCTAssertTrue(foreground, "Google Slides did not reach foreground")

        // Dump the accessibility tree for navigation/playback control discovery.
        let tree = slides.debugDescription
        print("=== SLIDES ACCESSIBILITY TREE BEGIN ===")
        print(tree)
        print("=== SLIDES ACCESSIBILITY TREE END ===")

        let treeAttachment = XCTAttachment(string: tree)
        treeAttachment.name = "slides-accessibility-tree.txt"
        treeAttachment.lifetime = .keepAlways
        add(treeAttachment)

        // Capture the current screen (expected: presentation slide 1 or editor).
        let shot = XCUIScreen.main.screenshot()
        let shotAttachment = XCTAttachment(screenshot: shot)
        shotAttachment.name = "slides-poc-current.png"
        shotAttachment.lifetime = .keepAlways
        add(shotAttachment)

        // Report what identifiable controls exist (informational, non-failing).
        let slideArea = slides.otherElements.count
        let buttons = slides.buttons.count
        print("=== POC COUNTS: otherElements=\(slideArea) buttons=\(buttons) ===")
    }
}
