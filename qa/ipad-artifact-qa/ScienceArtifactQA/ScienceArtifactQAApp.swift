import SwiftUI

@main
struct ScienceArtifactQAApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView(config: LaunchConfig.fromProcessInfo())
        }
    }
}
