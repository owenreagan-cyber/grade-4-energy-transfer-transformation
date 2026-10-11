import Combine
import Foundation
import PDFKit
import UIKit

/// Neutral background behind the PDF page so the white page edge is visible
/// but nothing distracts from content.
let kNeutralBackground = UIColor(white: 0.90, alpha: 1.0)

/// A PDFView that reapplies the requested scale on every layout pass so the
/// initial (and any subsequent) zoom is deterministic.
final class ScaledPDFView: PDFView {
    var onLayout: (() -> Void)?

    override func layoutSubviews() {
        super.layoutSubviews()
        onLayout?()
    }
}

/// Owns the PDFDocument and the PDFView, and exposes current page / page count
/// for the SwiftUI footer and for XCUITest assertions.
final class PDFSession: ObservableObject {
    @Published var currentPage: Int = 0
    @Published var pageCount: Int = 0
    @Published var scaleFactor: CGFloat = 0

    let pdfView = ScaledPDFView()
    var viewMode: ViewMode = .fitPage
    private var pageObserver: NSObjectProtocol?

    init() {
        configureView()
        pageObserver = NotificationCenter.default.addObserver(
            forName: .PDFViewPageChanged,
            object: pdfView,
            queue: .main
        ) { [weak self] _ in
            self?.refreshCurrentPage()
        }
    }

    private func configureView() {
        pdfView.autoScales = false
        pdfView.displayMode = .singlePage
        pdfView.displayDirection = .horizontal
        pdfView.displaysPageBreaks = false
        pdfView.pageShadowsEnabled = false
        pdfView.backgroundColor = kNeutralBackground
        pdfView.accessibilityIdentifier = "pdfView"
        pdfView.onLayout = { [weak self] in
            self?.applyScale()
        }
    }

    func load(url: URL) {
        let doc = PDFDocument(url: url)
        pdfView.document = doc
        pageCount = doc?.pageCount ?? 0
        pdfView.goToFirstPage(nil)
        currentPage = 1
        applyScale()
    }

    /// Apply fit-page / fit-width / actual scale against the first page's
    /// media box and the current view bounds. Deterministic: no animation,
    /// no auto-scaling.
    func applyScale() {
        guard let page = pdfView.document?.page(at: 0) else { return }
        let bounds = pdfView.bounds
        guard bounds.width > 0, bounds.height > 0 else { return }
        let pageSize = page.bounds(for: .mediaBox)
        guard pageSize.width > 0, pageSize.height > 0 else { return }

        let scale: CGFloat
        switch viewMode {
        case .fitPage:
            scale = min(bounds.width / pageSize.width, bounds.height / pageSize.height)
        case .fitWidth:
            scale = bounds.width / pageSize.width
        case .actual:
            scale = 1.0
        }
        pdfView.scaleFactor = scale
        scaleFactor = scale
    }

    func goToPage(_ index: Int) {
        guard let doc = pdfView.document, index >= 0, index < doc.pageCount else { return }
        guard let page = doc.page(at: index) else { return }
        pdfView.go(to: page) // instant jump, no scroll animation
        currentPage = index + 1 // deterministic fallback in case the notification is late
    }

    func nextPage() {
        goToPage(currentPage) // currentPage is 1-based; index = currentPage
    }

    func previousPage() {
        goToPage(currentPage - 2) // 1-based current minus 1 → 0-based index
    }

    private func refreshCurrentPage() {
        guard let current = pdfView.currentPage, let doc = pdfView.document else { return }
        currentPage = doc.index(for: current) + 1
    }

    deinit {
        if let observer = pageObserver {
            NotificationCenter.default.removeObserver(observer)
        }
    }
}
