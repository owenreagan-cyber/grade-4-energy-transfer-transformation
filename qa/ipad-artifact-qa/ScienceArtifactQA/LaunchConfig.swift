import Foundation
import UIKit

/// View modes the harness supports. Mirrors the manifest `viewMode` strings.
enum ViewMode: String, CaseIterable {
    case fitPage = "fit-page"
    case fitWidth = "fit-width"
    case actual = "actual"

    var label: String { rawValue }
}

/// Launch configuration read from the process launch arguments.
/// The XCUITest driver passes: `-artifactPath`, `-viewMode`, `-orientation`,
/// and (optional detail mode) `-detailPage`, `-detailScale`.
struct LaunchConfig {
    var artifactPath: String = ""
    var viewMode: ViewMode = .fitPage
    var orientation: String = "portrait"
    var page: Int? = nil
    var detailPage: Int? = nil
    var detailScale: Double? = nil

    static func fromProcessInfo() -> LaunchConfig {
        var config = LaunchConfig()
        let args = ProcessInfo.processInfo.arguments
        func value(after key: String) -> String? {
            guard let i = args.firstIndex(of: key), i + 1 < args.count else { return nil }
            return args[i + 1]
        }
        if let p = value(after: "-artifactPath") { config.artifactPath = p }
        if let m = value(after: "-viewMode") { config.viewMode = ViewMode(rawValue: m) ?? .fitPage }
        if let o = value(after: "-orientation") { config.orientation = o }
        if let d = value(after: "-page") { config.page = Int(d) }
        if let d = value(after: "-detailPage") { config.detailPage = Int(d) }
        if let s = value(after: "-detailScale") { config.detailScale = Double(s) }
        return config
    }

    var orientationMask: UIInterfaceOrientationMask {
        switch orientation {
        case "landscape": return .landscape
        case "portrait": return .portrait
        default: return .portrait
        }
    }
}
