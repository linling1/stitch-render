const puppeteer = require('puppeteer'),
        chromeLauncher = require('chrome-launcher'),
        CDP = require('chrome-remote-interface');


/*(async() => {
    const browser = await puppeteer.launch();
    console.log(await browser.version());
    browser.close();
})();*/

/*(async() => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto("https://dschnurr.medium.com/using-headless-chrome-as-an-automated-screenshot-tool-4b07dffba79a", {waitUntil: 'networkidle2'});
    await page.pdf({path: '/Users/linling/Desktop/page.pdf', format: 'A4'});

    browser.close();
})();*/


/**
 * Launches a debugging instance of Chrome.
 * @param {boolean=} headless True (default) launches Chrome in headless mode.
 *     False launches a full version of Chrome.
 * @return {Promise<ChromeLauncher>}
 */
function launchChrome(headless=true) {
    return chromeLauncher.launch({
        chromeFlags: [
            '--window-size=412,732',
            '--disable-gpu',
            headless ? '--headless' : ''
        ]
    });
}


/*launchChrome().then(async chrome => {
    const version = await CDP.Version({port: chrome.port});
    console.log(version['User-Agent']);
    chrome.kill();
});*/


/*(async function () {
    const chrome = await launchChrome();
    const protocol = await CDP({port: chrome.port});

    // Extract the DevTools protocol domains we need and enable them.
    // See API docs: https://chromedevtools.github.io/devtools-protocol/
    const {Page} = protocol;
    await Page.enable();

    Page.navigate({url: 'https://www.chromestatus.com/'});

    Page.loadEventFired(async () => {
        const manifest = await Page.getAppManifest();
        if (manifest.url) {
            console.log('Manifest: ' + manifest.url);
            console.log(manifest.data);
        } else {
            console.log('Site has no app manifest');
        }

        protocol.close();
        chrome.kill();      // Kill Chrome.
    });

})();*/


(async function () {

    const chrome = await launchChrome();
    const protocol = await CDP({port: chrome.port});

    // Extract the DevTools protocol domains we need and enable them.
    // See API docs: https://chromedevtools.github.io/devtools-protocol/
    const {Page, Runtime} = protocol;
    await Promise.all([Page.enable(), Runtime.enable()]);

    Page.navigate({url: 'https://dschnurr.medium.com/using-headless-chrome-as-an-automated-screenshot-tool-4b07dffba79a'});

    // Wait for window.onload before doing stuff.
    Page.loadEventFired(async () => {
        const js = "document.querySelector('title').textContent";
        // Evaluate the JS expression in the page.
        const result = await Runtime.evaluate({expression: js});
        console.log('Title of page: ' + result.result.value);

        protocol.close();
        chrome.kill();      // Kill Chrome.
    })

})();


/*(async function () {
    const chrome = await launchChrome();
    const protocol = await CDP({port: chrome.port});

    const {Network, Page, Runtime} = protocol;
    // setup handlers
    Network.requestWillBeSent((params) => {
        console.log(params.request.url);
    });
    Page.loadEventFired(async() => {
        const js = "document.querySelector('title').textContent";
        // Evaluate the JS expression in the page.
        const result = await Runtime.evaluate({expression: js});
        console.log('Title of page: ' + result.result.value);
        console.log("22222222")
        protocol.close();
    });
    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable(),
        Runtime.enable()
    ]).then(() => {
        console.log("1111111")
        return Page.navigate({url: 'https://github.com'});
    }).catch((err) => {
        console.error(err);
        protocol.close();
    });

})();*/








