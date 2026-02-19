#!/usr/bin/env node
/**
 * Export HTML slides to PDF.
 *
 * Usage: node export-pdf.js <input.html> <output.pdf>
 *
 * Renders each .slide element as a 1920x1080 page.
 */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function exportPDF(inputPath, outputPath) {
  const absoluteInput = path.resolve(inputPath);
  if (!fs.existsSync(absoluteInput)) {
    console.error(`File not found: ${absoluteInput}`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`file://${absoluteInput}`, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outputPath,
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  await browser.close();
  console.log(`PDF exported to ${outputPath}`);
}

const [,, input, output] = process.argv;
if (!input || !output) {
  console.error('Usage: node export-pdf.js <input.html> <output.pdf>');
  process.exit(1);
}
exportPDF(input, output);
