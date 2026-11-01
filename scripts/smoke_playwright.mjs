// Headless smoke test: every storybook and mini-game renders with 0 console errors.
// Needs Playwright available to node (not a repo dependency). Default target is the
// files on disk (file://). To test a served copy instead, start a server and pass its URL:
//   python3 -m http.server 8000
//   node scripts/smoke_playwright.mjs http://localhost:8000/
import { chromium } from 'playwright';
import { readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = process.argv[2] || pathToFileURL(root + '/').href;
const pages = ['books', 'games'].flatMap(dir =>
  readdirSync(join(root, dir))
    .filter(f => f.endsWith('.html'))
    .sort()
    .map(f => `${dir}/${f}`)
);

const browser = await chromium.launch();
let failed = 0;
for (const path of pages) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(`pageerror: ${err.message}`));
  let status = 'ERR';
  try {
    const response = await page.goto(new URL(path, base).href, { waitUntil: 'load', timeout: 30000 });
    status = response ? response.status() : 'no-response';
    await page.waitForTimeout(1000);
  } catch (err) {
    errors.push(`navigation: ${err.message.split('\n')[0]}`);
  }
  const ok = status === 200 && errors.length === 0;
  if (!ok) failed++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${path} status=${status} errors=${errors.length}`);
  for (const e of errors) console.log(`     - ${e}`);
  await context.close();
}
await browser.close();
console.log(`\n${pages.length - failed}/${pages.length} pages passed`);
process.exitCode = failed ? 1 : 0;
