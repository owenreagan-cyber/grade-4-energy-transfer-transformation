import CryptoKit
import Foundation
import UIKit
import XCTest

/// Shared support for the UI-test harness: loads the run config + manifest from
/// the host filesystem (the simulator shares the macOS filesystem), and writes
/// deterministic screenshots + metadata back to the host.
struct TestSupport {
    let repoRoot: URL
    let runConfig: RunConfig
    let manifest: Manifest

    // MARK: - Loading

    static func load() throws -> TestSupport {
        // #filePath = <repo>/qa/ipad-artifact-qa/ScienceArtifactQAUITests/TestSupport.swift
        let source = URL(fileURLWithPath: #filePath)
        let repoRoot = source
            .deletingLastPathComponent() // ScienceArtifactQAUITests
            .deletingLastPathComponent() // qa/ipad-artifact-qa
            .deletingLastPathComponent() // qa
            .deletingLastPathComponent() // repo root
        let configURL = repoRoot
            .appendingPathComponent("qa/temp/ipad-artifact-qa/current-run.json")
        let data = try Data(contentsOf: configURL)
        let runConfig = try JSONDecoder().decode(RunConfig.self, from: data)
        let manifestURL = URL(fileURLWithPath: runConfig.manifestPath)
        let manifestData = try Data(contentsOf: manifestURL)
        let manifest = try JSONDecoder().decode(Manifest.self, from: manifestData)
        return TestSupport(repoRoot: repoRoot, runConfig: runConfig, manifest: manifest)
    }

    func prepareOutput() throws {
        let fm = FileManager.default
        let screenshots = runConfig.outputDir.appendingPathComponent("screenshots", isDirectory: true)
        try fm.createDirectory(at: screenshots, withIntermediateDirectories: true)
    }

    // MARK: - Helpers

    func absoluteSource(_ relativePath: String) -> URL {
        repoRoot.appendingPathComponent(relativePath)
    }

    /// Deterministic screenshot filename:
    /// `<artifactId>__<deviceSlug>__<orientation>__<viewMode>__<p|s><nnn>.png`
    func screenshotName(artifact: Artifact, page: Int) -> String {
        let prefix = artifact.artifactType == "SLIDE_PDF" ? "s" : "p"
        let viewMode = artifact.viewMode.replacingOccurrences(of: "_", with: "-")
        return String(
            format: "%@__%@__%@__%@__%@%03d.png",
            artifact.artifactId,
            runConfig.deviceSlug,
            artifact.orientation,
            viewMode,
            prefix,
            page
        )
    }

    func screenshotURL(artifact: Artifact, page: Int) -> URL {
        runConfig.outputDir
            .appendingPathComponent("screenshots", isDirectory: true)
            .appendingPathComponent(screenshotName(artifact: artifact, page: page))
    }

    /// The capture plan from the run config, or (backward-compatible fallback)
    /// the full manifest when no plan was supplied.
    func capturePlanItems() -> [CapturePlanItem] {
        if let plan = runConfig.capturePlan, !plan.isEmpty {
            return plan
        }
        return manifest.artifacts.map { CapturePlanItem(artifactId: $0.artifactId, pages: nil) }
    }

    /// Write launch/load/capture efficiency counters for the driver to report.
    func writeHarnessStats(launchCount: Int, artifactLoads: Int, captureCount: Int) throws {
        let stats: [String: Int] = [
            "launchCount": launchCount,
            "artifactLoads": artifactLoads,
            "captureCount": captureCount,
        ]
        let data = try JSONSerialization.data(withJSONObject: stats, options: [.prettyPrinted])
        let url = runConfig.outputDir.appendingPathComponent("harness-stats.json")
        try data.write(to: url)
    }

    func viewportPixels() -> [String: Int] {
        let bounds = UIScreen.main.bounds
        let scale = UIScreen.main.scale
        return [
            "width": Int(bounds.width * scale),
            "height": Int(bounds.height * scale),
        ]
    }

    static func sha256(_ data: Data) -> String {
        SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }

    /// True pixel dimensions of a PNG, read from the IHDR header bytes.
    /// `CGImageSource` reports swapped width/height for iOS screenshots (it
    /// honors an embedded orientation), and `XCUIScreenshot.image.size` is not
    /// orientation-adjusted either. The encoded PNG bytes are ground truth.
    static func pixelSize(ofPNG data: Data) -> [String: Int]? {
        // PNG: 8-byte signature, then IHDR (len@8, "IHDR"@12, width@16, height@20).
        let signature: [UInt8] = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
        guard data.count >= 24 else { return nil }
        let bytes = [UInt8](data)
        guard Array(bytes[0..<8]) == signature,
              bytes[12] == 0x49, bytes[13] == 0x48, bytes[14] == 0x44, bytes[15] == 0x52 else {
            return nil
        }
        func u32(_ offset: Int) -> Int {
            (Int(bytes[offset]) << 24) | (Int(bytes[offset + 1]) << 16) |
            (Int(bytes[offset + 2]) << 8) | Int(bytes[offset + 3])
        }
        return ["width": u32(16), "height": u32(20)]
    }

    func appendRecord(_ record: CaptureRecord) throws {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        var line = try encoder.encode(record)
        line.append(0x0A) // newline
        let file = runConfig.outputDir.appendingPathComponent("capture.jsonl")
        if FileManager.default.fileExists(atPath: file.path) {
            let handle = try FileHandle(forWritingTo: file)
            defer { try? handle.close() }
            try handle.seekToEnd()
            try handle.write(contentsOf: line)
        } else {
            try line.write(to: file)
        }
    }

    /// Read back capture records as typed models (for cross-test assertions).
    func readCaptureRecords() throws -> [CaptureRecord] {
        let file = runConfig.outputDir.appendingPathComponent("capture.jsonl")
        guard FileManager.default.fileExists(atPath: file.path) else { return [] }
        let text = try String(contentsOf: file, encoding: .utf8)
        let decoder = JSONDecoder()
        return text.split(separator: "\n").compactMap { line -> CaptureRecord? in
            guard let data = line.data(using: .utf8) else { return nil }
            return try? decoder.decode(CaptureRecord.self, from: data)
        }
    }
}

// MARK: - Codable models

struct RunConfig: Codable {
    let runId: String
    let buildId: String
    let manifestPath: String
    let outputDirPath: String
    let deviceModel: String
    let deviceSlug: String
    let osVersion: String
    let mode: String?
    let evidenceClass: String?
    let capturePlan: [CapturePlanItem]?

    var outputDir: URL { URL(fileURLWithPath: outputDirPath) }
}

/// One artifact in the capture plan. ``pages`` is nil when every page/slide is
/// required; otherwise it is the exact ordered page list to capture.
struct CapturePlanItem: Codable {
    let artifactId: String
    let pages: [Int]?
}

struct Manifest: Codable {
    let schema: String
    let chapter: Int
    let buildId: String
    let artifacts: [Artifact]

    func artifact(byId id: String) -> Artifact? {
        artifacts.first { $0.artifactId == id }
    }
}

struct Artifact: Codable {
    let artifactId: String
    let artifactType: String
    let sourcePath: String
    let masterPath: String?
    let artifactSHA256: String
    let expectedPages: Int
    let orientation: String
    let viewMode: String
    let studentOrTeacher: String
    let chapter: Int
}

struct CaptureRecord: Codable {
    let artifactId: String
    let artifactType: String
    let artifactSHA256: String
    let pdfPage: Int
    let deviceModel: String
    let osVersion: String
    let viewportPixels: [String: Int]
    let orientation: String
    let viewMode: String
    let zoomScale: Double?
    let screenshotSHA256: String
    let screenshotPath: String
    let runId: String
    let buildId: String
}
