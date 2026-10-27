const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')console.log('BROWSER',m.text())});
 await page.route('**/*',route=>{const url=new URL(route.request().url());if(url.pathname.startsWith('/static/')){const file=path.join(process.cwd(),url.pathname.slice(1));return route.fulfill({path:file});}return route.fulfill({contentType:'text/html',body:fs.readFileSync(process.argv[2] || path.join(process.env.TEMP,'qmp-export-fixture.html'),'utf8')});});
 await page.goto('http://qmp.local/presentacion/?semana=2026-W41');
 await page.locator('#select-none').click();assert(await page.locator('#export-pdf').isDisabled());
 for(const id of ['lines','requirement_profile','compliance_timeline'])await page.locator(`#chart-options input[value="${id}"]`).check({force:true});
 await page.locator('#charts-per-page').selectOption('2');
 await page.locator('#next-slide').click();const before=await page.locator('#slide-status').textContent();
 for(const format of ['pdf','pptx']){
 const download=page.waitForEvent('download',{timeout:120000});await page.locator('#export-'+format).click();
 const result=await download;await result.saveAs(path.join(process.env.TEMP,'qmp-export.'+format));
 assert.equal(await page.locator('#slide-status').textContent(),before);assert(!(await page.locator('#export-'+format).isDisabled()));
 console.log(format,fs.statSync(path.join(process.env.TEMP,'qmp-export.'+format)).size);
 }
 await page.locator('#previous-slide').click();await page.screenshot({path:path.join(process.env.TEMP,'qmp-export-preview.png'),fullPage:true});
 assert.deepEqual(errors,[]);console.log('Exports and state restoration passed');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
