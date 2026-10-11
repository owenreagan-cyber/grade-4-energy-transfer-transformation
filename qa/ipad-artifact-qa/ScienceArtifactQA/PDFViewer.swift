import SwiftUI
import PDFKit

/// Wraps the shared PDFView from PDFSession so SwiftUI can host it without
/// re-creating the view (which would lose document + scale state).
struct PDFViewer: UIViewRepresentable {
    let session: PDFSession
    let viewMode: ViewMode

    func makeUIView(context: Context) -> PDFView {
        session.pdfView
    }

    func updateUIView(_ uiView: PDFView, context: Context) {
        session.viewMode = viewMode
        session.applyScale()
    }
}
