const url = require('url');
const fetch = require('node-fetch');
const { Random } = require("random-js");
const random = new Random();

const util = exports = module.exports = {};

const PROXY_ONLINE_API = "http://spider-online-goproxy.crawler.svc.k8sc1.nb.com:3140/proxy/list";
const PROXY_OFFLINE_API = "http://spider-offline-goproxy.crawler.svc.k8sc1.nb.com:3140/proxy/list";
const USER_AGENT_POOL = [
	// "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    // "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    // "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    // "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)",
    // "ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
]

// Normalizes unimportant differences in URLs - e.g. ensures
// http://google.com/ and http://google.com normalize to the same string
util.normalizeUrl = function(u) {
	return url.format(url.parse(u, true));
};

util.getOptions = function(req) {

	var requestedUrl = req.url;

	//new API starts with render so we'll parse the URL differently if found
	if(requestedUrl.indexOf('/render') === 0) {

		let optionsObj = {};
		if(req.method === 'GET') {
			optionsObj = url.parse(requestedUrl, true).query;
		} else if (req.method === 'POST') {
			optionsObj = req.body;
		}

		return {
			// url: util.getUrl(optionsObj.url),
			url: optionsObj.url,
			renderType: optionsObj.renderType || 'html',
			userAgent: optionsObj.userAgent,
			fullpage: optionsObj.fullpage === 'true',
			width: optionsObj.width,
			height: optionsObj.height,
			followRedirects: optionsObj.followRedirects === 'true',
			javascript: optionsObj.javascript,
			sunflower: optionsObj.sunflower === 'true',
			disableImage: optionsObj.disableImage === 'true',
			waitAfterLastRequest: optionsObj.delay && optionsObj.delay * 1000,
			parseShadowDom: optionsObj.parseShadowDom === 'true',
			proxyUrl: optionsObj.proxyUrl,
			disableProxy: optionsObj.disableProxy === 'true'
		}

	} else {

		return {
			url: util.getUrl(requestedUrl),
			renderType: 'html'
		}
	}
}

// Gets the URL to prerender from a request, stripping out unnecessary parts
util.getUrl = function(requestedUrl) {
	var decodedUrl, realUrl = requestedUrl,
		parts;

	if (!requestedUrl) {
		return '';
	}

	realUrl = realUrl.replace(/^\//, '');

	try {
		decodedUrl = decodeURIComponent(realUrl);
	} catch (e) {
		decodedUrl = realUrl;
	}

	//encode a # for a non #! URL so that we access it correctly
	decodedUrl = this.encodeHash(decodedUrl);

	//if decoded url has two query params from a decoded escaped fragment for hashbang URLs
	if (decodedUrl.indexOf('?') !== decodedUrl.lastIndexOf('?')) {
		decodedUrl = decodedUrl.substr(0, decodedUrl.lastIndexOf('?')) + '&' + decodedUrl.substr(decodedUrl.lastIndexOf('?') + 1);
	}

	parts = url.parse(decodedUrl, true);

	// Remove the _escaped_fragment_ query parameter
	if (parts.query && parts.query['_escaped_fragment_'] !== undefined) {

		if (parts.query['_escaped_fragment_'] && !Array.isArray(parts.query['_escaped_fragment_'])) {
			parts.hash = '#!' + parts.query['_escaped_fragment_'];
		}

		delete parts.query['_escaped_fragment_'];
		delete parts.search;
	}

	// Bing was seen accessing a URL like /?&_escaped_fragment_=
	delete parts.query[''];

	var newUrl = url.format(parts);

	//url.format encodes spaces but not arabic characters. decode it here so we can encode it all correctly later
	try {
		newUrl = decodeURIComponent(newUrl);
	} catch (e) {}

	newUrl = this.encodeHash(newUrl);

	return newUrl;
};

util.encodeHash = function(url) {
	if (url.indexOf('#!') === -1 && url.indexOf('#') >= 0) {
		url = url.replace(/#/g, '%23');
	}

	return url;
}

util.log = function() {
	if (process.env.DISABLE_LOGGING) {
		return;
	}

	console.log.apply(console.log, [new Date().toISOString()].concat(Array.prototype.slice.call(arguments, 0)));
	for (var i = 0; i < arguments.length; i++) {
		if (arguments[i] instanceof Error) {
			console.log(arguments[i].stack);
		}
	}
};


util.gainProxyUrl = async function () {
	let resp = await fetch(PROXY_OFFLINE_API);
	let jresp = await resp.json();
	if (jresp.code != 0) {
		return undefined;
	}

	let proxyList = jresp.result;
	if (proxyList.length == 0) {
		return undefined;
	}
	let i = random.integer(0, proxyList.length-1);
	return proxyList[i];
};


util.gainUserAgent = function() {
	if (USER_AGENT_POOL.length == 0) {
		return undefined;
	}
	if (USER_AGENT_POOL.length == 1) {
		return USER_AGENT_POOL[0];
	}
	let i = random.integer(0, USER_AGENT_POOL.length-1)
	return USER_AGENT_POOL[i];
}