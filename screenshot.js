const puppeteer = require('puppeteer');
const path = require('path');

const file = process.argv[2] || 'index.html';
const output = process.argv[3] || 'screenshot.png';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto('file://' + path.resolve(file));
  await page.screenshot({ path: output, fullPage: true });
  await browser.close();
  console.log(`Saved: ${output}`);
})();
