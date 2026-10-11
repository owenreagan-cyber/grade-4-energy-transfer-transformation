import XCTest

/// Full 48-slide walkthrough of the Chapter 1 presentation in Google Slides
/// present mode on a physical iPad.
///
/// Strategy (discovered in POC #3):
///   - Enter present mode: "Start presentation" → "Present on this device".
///   - Each slide exposes an Image labeled "Slide N of 48:" plus the slide text
///     as accessible Image labels. Swiping left advances one slide.
///   - Stop (assert-fail) on any position mismatch; never blindly continue.
final class SlidesWalkthrough: XCTestCase {

    let totalSlides = 48
    let videoSlides: Set<Int> = [8, 27, 28]

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
        let att = XCTAttachment(string: app.debugDescription)
        att.name = name
        att.lifetime = .keepAlways
        add(att)
        print("=== \(name) ===\n\(app.debugDescription)")
    }

    private func enterPresentMode(_ slides: XCUIApplication) {
        // If a prior run left the app in present mode, exit it first.
        // Controls auto-hide, so reveal them ("Show controls") then end.
        let showControls = slides.buttons["Show controls"]
        if showControls.exists {
            showControls.tap()
            sleep(1)
        }
        let end = slides.buttons["End presentation"]
        if end.exists {
            end.tap()
            sleep(2)
        }

        let start = slides.buttons["Start presentation"]
        XCTAssertTrue(start.waitForExistence(timeout: 15), "Start presentation button missing")
        start.tap()
        sleep(1)

        let onDevice = slides.cells["Present on this device"].firstMatch
        if onDevice.waitForExistence(timeout: 5) {
            onDevice.tap()
        } else {
            let label = slides.staticTexts["Present on this device"].firstMatch
            XCTAssertTrue(label.waitForExistence(timeout: 5), "Present on this device option missing")
            label.tap()
        }
        sleep(4)
    }

    private func positionIndicator(_ slides: XCUIApplication, _ n: Int) -> XCUIElement {
        slides.images
            .matching(NSPredicate(format: "label BEGINSWITH %@", "Slide \(n) of \(totalSlides)"))
            .firstMatch
    }

    /// Bounded video interaction: tap Play, capture, tap Pause, capture, then
    /// Play again (resume) and capture. Does not claim audio verification.
    private func exerciseVideo(_ slides: XCUIApplication, _ n: Int) {
        let play = slides.buttons["Play"].firstMatch
        if play.waitForExistence(timeout: 5) {
            play.tap()
            sleep(2)
            snapshot(String(format: "video-slide-%02d-playing.png", n))

            // Pause (the button relabels to "Pause" once playing).
            let pause = slides.buttons["Pause"].firstMatch
            if pause.waitForExistence(timeout: 3) {
                pause.tap()
                sleep(1)
                snapshot(String(format: "video-slide-%02d-paused.png", n))

                // Resume.
                let playAgain = slides.buttons["Play"].firstMatch
                if playAgain.waitForExistence(timeout: 3) {
                    playAgain.tap()
                    sleep(2)
                    snapshot(String(format: "video-slide-%02d-resumed.png", n))
                } else {
                    add(XCTAttachment(string: "no Play-after-pause on slide \(n)").then { $0.name = String(format: "video-slide-%02d-resume-note.txt", n); $0.lifetime = .keepAlways })
                }
            } else {
                add(XCTAttachment(string: "no Pause button after Play on slide \(n)").then { $0.name = String(format: "video-slide-%02d-pause-note.txt", n); $0.lifetime = .keepAlways })
            }
        } else {
            add(XCTAttachment(string: "no Play button on slide \(n)").then { $0.name = String(format: "video-slide-%02d-play-note.txt", n); $0.lifetime = .keepAlways })
        }
    }

    private func advance(_ slides: XCUIApplication) {
        // Swipe in the upper slide area (y ≈ 0.22), ABOVE any embedded video
        // player, so the gesture advances the deck instead of being consumed
        // by the video (videos occupy the vertical center).
        let from = slides.coordinate(withNormalizedOffset: CGVector(dx: 0.8, dy: 0.22))
        let to = slides.coordinate(withNormalizedOffset: CGVector(dx: 0.2, dy: 0.22))
        from.press(forDuration: 0.05, thenDragTo: to)
        sleep(2)
    }

    func testWalkthroughAll48Slides() throws {
        let slides = XCUIApplication(bundleIdentifier: "com.google.Slides")
        slides.activate()
        XCTAssertTrue(slides.wait(for: .runningForeground, timeout: 30))

        enterPresentMode(slides)

        // Give present mode a generous load window for slide 1.
        let firstIndicator = positionIndicator(slides, 1)
        if !firstIndicator.waitForExistence(timeout: 20) {
            dumpTree("present-mode-entry-failure.txt", slides)
            XCTFail("Slide 1 position label not found after present-mode entry; tree dumped")
        }

        var captured: [Int] = []
        for n in 1...totalSlides {
            // 1. Verify position.
            let indicator = positionIndicator(slides, n)
            if !indicator.waitForExistence(timeout: 10) {
                dumpTree(String(format: "position-failure-%02d.txt", n), slides)
                XCTFail("Slide \(n) position label not found (expected 'Slide \(n) of \(totalSlides):'); tree dumped")
            }
            captured.append(n)

            // 2. Capture the slide.
            snapshot(String(format: "slide-%02d.png", n))

            // 3. On video slides, dump the accessibility tree for playback
            //    control discovery, then exercise play/pause/resume.
            if videoSlides.contains(n) {
                dumpTree(String(format: "video-slide-%02d-tree.txt", n), slides)
                exerciseVideo(slides, n)
            }

            // 4. Advance to the next slide (unless this is the last).
            if n < totalSlides {
                advance(slides)
            }
        }

        print("=== WALKTHROUGH CAPTURED: \(captured.count) slides ===")
        add(XCTAttachment(string: "captured: \(captured)").then {
            $0.name = "walkthrough-summary.txt"; $0.lifetime = .keepAlways
        })
        XCTAssertEqual(captured.count, totalSlides, "walkthrough did not capture all slides")
    }
}

private extension XCTAttachment {
    func then(_ block: (XCTAttachment) -> Void) -> XCTAttachment {
        block(self)
        return self
    }
}
