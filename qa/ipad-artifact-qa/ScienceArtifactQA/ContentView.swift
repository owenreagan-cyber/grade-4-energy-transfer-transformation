import SwiftUI
import UIKit

struct ContentView: View {
    let config: LaunchConfig
    @StateObject private var session = PDFSession()
    @State private var loadError: String?

    var body: some View {
        VStack(spacing: 0) {
            if let error = loadError {
                VStack {
                    Text("LOAD ERROR").font(.headline)
                    Text(error)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                        .padding()
                        .accessibilityIdentifier("loadError")
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if session.pageCount > 0 {
                PDFViewer(session: session, viewMode: config.viewMode)
                    .accessibilityIdentifier("pdfView")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                ProgressView("Loading PDF…")
                    .accessibilityIdentifier("loading")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }

            // Minimal, non-overlapping footer: page indicator + navigation.
            // Sits BELOW the PDF view so it never hides content.
            footer
        }
        .background(Color(kNeutralBackground))
        .onAppear {
            lockOrientation(config.orientationMask)
            loadPDF()
        }
        .onChange(of: config.viewMode) { newMode in
            session.viewMode = newMode
            session.applyScale()
        }
    }

    private var footer: some View {
        HStack(spacing: 16) {
            Button {
                session.previousPage()
            } label: {
                Text("Prev")
                    .frame(minWidth: 56, minHeight: 30)
            }
            .buttonStyle(.bordered)
            .accessibilityIdentifier("prevButton")

            Text(session.pageCount > 0
                 ? "Page \(session.currentPage) of \(session.pageCount)"
                 : "Page – of –")
                .font(.footnote.monospacedDigit())
                .foregroundColor(.secondary)
                .accessibilityIdentifier("pageIndicator")

            Button {
                session.nextPage()
            } label: {
                Text("Next")
                    .frame(minWidth: 56, minHeight: 30)
            }
            .buttonStyle(.bordered)
            .accessibilityIdentifier("nextButton")

            Spacer()

            Text(String(format: "%@ · %@ · x%.3f",
                        config.viewMode.label,
                        config.orientation,
                        session.scaleFactor))
                .font(.caption2)
                .foregroundColor(.secondary)
                .accessibilityIdentifier("modeLabel")
        }
        .padding(.horizontal, 16)
        .frame(height: 44)
        .background(Color(kNeutralBackground))
        .overlay(Divider(), alignment: .top)
    }

    private func loadPDF() {
        guard !config.artifactPath.isEmpty else {
            loadError = "No -artifactPath launch argument provided."
            return
        }
        let url = URL(fileURLWithPath: config.artifactPath)
        guard FileManager.default.fileExists(atPath: url.path) else {
            loadError = "File not found: \(url.path)"
            return
        }
        session.load(url: url)
        if session.pageCount == 0 {
            loadError = "Could not open PDF (malformed or empty): \(url.path)"
            return
        }

        if let page = config.page {
            session.goToPage(page - 1)
        } else if let detail = config.detailPage {
            session.viewMode = .actual
            session.goToPage(detail - 1)
            if let scale = config.detailScale {
                session.pdfView.scaleFactor = CGFloat(scale)
            }
        }
    }

    /// Lock the app to the requested orientation for deterministic screenshots.
    private func lockOrientation(_ mask: UIInterfaceOrientationMask) {
        guard let scene = UIApplication.shared.connectedScenes
            .compactMap({ $0 as? UIWindowScene })
            .first else { return }
        scene.requestGeometryUpdate(.iOS(interfaceOrientations: mask)) { error in
            print("orientation request error: \(error)")
        }
    }
}
