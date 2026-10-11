import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';

const inputFile = process.argv[2];
const outputFile = process.argv[3] || (inputFile ? inputFile.replace(/\.html?$/, '.pdf') : null);

if (!inputFile) {
  console.error('Usage: node render-pdf.js <input.html> [output.pdf]');
  process.exit(1);
}

const inputPath = path.resolve(inputFile);
const outputPath = path.resolve(outputFile);

if (!fs.existsSync(inputPath)) {
  console.error(`File not found: ${inputPath}`);
  process.exit(1);
}

async function render() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(`file://${inputPath}`, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '20mm',
      bottom: '20mm',
      left: '15mm',
      right: '15mm',
    },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `
      <div style="font-size: 9px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #888; width: 100%; padding: 0 15mm; display: flex; justify-content: space-between;">
        <span>Generated via Cursor Workspace</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div>
    `,
  });

  await browser.close();
  console.log(`✓ Successfully compiled: ${outputPath}`);
}

render().catch((err) => {
  console.error('Render error:', err);
  process.exit(1);
});
