// Test if Playwright can actually run
const { chromium } = require('playwright');

(async () => {
    try {
        console.log('🧪 Testing Playwright capabilities...');

        const browser = await chromium.launch({
            headless: true
        });

        console.log('✅ Browser launched');

        const page = await browser.newPage();
        console.log('✅ Page created');

        await page.setContent('<html><body><h1>Test</h1></body></html>');
        const title = await page.textContent('h1');
        console.log('✅ Content set:', title);

        await page.screenshot({ path: '/tmp/test-screenshot.png' });
        console.log('✅ Screenshot taken');

        await browser.close();
        console.log('✅ Browser closed');

        console.log('\n🎉 SUCCESS: Playwright is fully functional!');
        process.exit(0);
    } catch (error) {
        console.error('❌ FAILED:', error.message);
        console.error('Full error:', error);
        process.exit(1);
    }
})();
