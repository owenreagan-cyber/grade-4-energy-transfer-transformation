import XCTest

/// Focused video interaction: navigate to slide 8, then play → pause → resume,
/// dumping the accessibility tree at each state to discover the resume control.
final class VideoInteraction: XCTestCase {

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
        add(XCTAttachment(string: app.debugDescription).then {
            $0.name = name; $0.lifetime = .keepAlways
        })
    }

    private func swipeForward(_ slides: XCUIApplication) {
        let from = slides.coordinate(withNormalizedOffset: CGVector(dx: 0.8, dy: 0.22))
        let to = slides.coordinate(withNormalizedOffset: CGVector(dx: 0.2, dy: 0.22))
        from.press(forDuration: 0.05, thenDragTo: to)
        sleep(2)
    }

    func testVideoPlayPauseResume() throws {
        let slides = XCUIApplication(bundleIdentifier: "com.google.Slides")
        slides.activate()
        XCTAssertTrue(slides.wait(for: .runningForeground, timeout: 30))

        // Reset out of present mode if a prior run left it there.
        if slides.buttons["Show controls"].exists { slides.buttons["Show controls"].tap(); sleep(1) }
        if slides.buttons["End presentation"].exists { slides.buttons["End presentation"].tap(); sleep(2) }

        // Enter present mode.
        let start = slides.buttons["Start presentation"]
        XCTAssertTrue(start.waitForExistence(timeout: 15), "no Start presentation")
        start.tap(); sleep(1)
        let onDevice = slides.cells["Present on this device"].firstMatch
        if onDevice.waitForExistence(timeout: 5) { onDevice.tap() }
        else { slides.staticTexts["Present on this device"].firstMatch.tap() }
        sleep(4)

        // Navigate to slide 8 (7 swipes from slide 1).
        for _ in 1...7 { swipeForward(slides) }
        let s8 = slides.images.matching(NSPredicate(format: "label BEGINSWITH %@", "Slide 8 of 48")).firstMatch
        XCTAssertTrue(s8.waitForExistence(timeout: 8), "not on slide 8")
        snapshot("v08-before.png")
        dumpTree("v08-before-tree.txt", slides)

        // Play.
        let play = slides.buttons["Play"].firstMatch
        XCTAssertTrue(play.waitForExistence(timeout: 5), "no Play button")
        play.tap(); sleep(2)
        snapshot("v08-playing.png")
        dumpTree("v08-playing-tree.txt", slides)

        // Pause (relabeled button).
        let pause = slides.buttons["Pause"].firstMatch
        XCTAssertTrue(pause.waitForExistence(timeout: 5), "no Pause button")
        pause.tap(); sleep(1)
        snapshot("v08-paused.png")
        dumpTree("v08-paused-tree.txt", slides)

        // Resume: try labelled button, then coordinate fallback on video center.
        let resume = slides.buttons["Play"].firstMatch
        if resume.waitForExistence(timeout: 4) {
            resume.tap()
        } else {
            // coordinate fallback: center of the video area
            slides.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap()
        }
        sleep(2)
        snapshot("v08-resumed.png")
        dumpTree("v08-resumed-tree.txt", slides)
    }
}

private extension XCTAttachment {
    func then(_ block: (XCTAttachment) -> Void) -> XCTAttachment {
        block(self)
        return self
    }
}
