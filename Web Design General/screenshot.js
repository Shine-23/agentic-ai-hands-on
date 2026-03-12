const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  const filePath = 'file:///' + path.resolve('index.html').split('\\').join('/');
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 15000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: 'screenshot_v1.png', fullPage: true });
  await browser.close();
  console.log('Screenshot saved to screenshot_v1.png');
})();
