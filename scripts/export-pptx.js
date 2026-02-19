#!/usr/bin/env node
/**
 * Export HTML slides to PPTX.
 *
 * Usage: node export-pptx.js <input.html> <output.pptx>
 *
 * Reads each .slide element from the HTML, captures a screenshot
 * via Puppeteer, and places each as a full-bleed image slide in a PPTX.
 */
const PptxGenJS = require('pptxgenjs');
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function exportPPTX(inputPath, outputPath) {
  const absoluteInput = path.resolve(inputPath);
  if (!fs.existsSync(absoluteInput)) {
    console.error(`File not found: ${absoluteInput}`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`file://${absoluteInput}`, { waitUntil: 'networkidle0' });

  const slideCount = await page.evaluate(() =>
    document.querySelectorAll('.slide').length
  );

  if (slideCount === 0) {
    console.error('No .slide elements found in input HTML');
    await browser.close();
    process.exit(1);
  }

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE', width: 13.333, height: 7.5 });
  pptx.layout = 'WIDE';

  for (let i = 0; i < slideCount; i++) {
    const imgData = await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide');
      const slide = slides[idx];
      slide.scrollIntoView();
      return null;
    }, i);

    const slideEl = await page.$(`.slide:nth-child(${i + 1})`);
    const screenshot = await slideEl.screenshot({ encoding: 'base64' });

    const pptxSlide = pptx.addSlide();
    pptxSlide.addImage({
      data: `image/png;base64,${screenshot}`,
      x: 0,
      y: 0,
      w: '100%',
      h: '100%'
    });
  }

  await browser.close();
  await pptx.writeFile({ fileName: outputPath });
  console.log(`PPTX exported to ${outputPath}`);
}

const [,, input, output] = process.argv;
if (!input || !output) {
  console.error('Usage: node export-pptx.js <input.html> <output.pptx>');
  process.exit(1);
}
exportPPTX(input, output);
