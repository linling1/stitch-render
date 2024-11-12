const util = require('./util.js');
const validUrl = require('valid-url');
const { v4: uuidv4 } = require('uuid');
const { json } = require('body-parser');

const WAIT_AFTER_LAST_REQUEST = process.env.WAIT_AFTER_LAST_REQUEST || 500;

const PAGE_DONE_CHECK_INTERVAL = process.env.PAGE_DONE_CHECK_INTERVAL || 500;

const PAGE_LOAD_TIMEOUT = process.env.PAGE_LOAD_TIMEOUT || 20 * 1000;

const FOLLOW_REDIRECTS = process.env.FOLLOW_REDIRECTS || false;

const LOG_REQUESTS = process.env.LOG_REQUESTS || false;

const CAPTURE_CONSOLE_LOG = process.env.CAPTURE_CONSOLE_LOG || false;

const ENABLE_SERVICE_WORKER = process.env.ENABLE_SERVICE_WORKER || false;

//try to restart the browser only if there are zero requests in flight
const BROWSER_TRY_RESTART_PERIOD = process.env.BROWSER_TRY_RESTART_PERIOD || 600000;

const BROWSER_DEBUGGING_PORT = process.env.BROWSER_DEBUGGING_PORT || 9222;

const TIMEOUT_STATUS_CODE = process.env.TIMEOUT_STATUS_CODE;

const PARSE_SHADOW_DOM = process.env.PARSE_SHADOW_DOM || false;

const ENBALE_PROXY_POOL = process.env.ENBALE_PROXY_POOL === 'true' || false

const server = exports = module.exports = {};



server.init = function(options) {
	this.plugins = this.plugins || [];
	this.options = options || {};

	this.options.waitAfterLastRequest = this.options.waitAfterLastRequest || WAIT_AFTER_LAST_REQUEST;
	this.options.pageDoneCheckInterval = this.options.pageDoneCheckInterval || PAGE_DONE_CHECK_INTERVAL;
	this.options.pageLoadTimeout = this.options.pageLoadTimeout || PAGE_LOAD_TIMEOUT;
	this.options.followRedirects = this.options.followRedirects || FOLLOW_REDIRECTS;
	this.options.logRequests = this.options.logRequests || LOG_REQUESTS;
	this.options.captureConsoleLog = this.options.captureConsoleLog || CAPTURE_CONSOLE_LOG;
	this.options.enableServiceWorker = this.options.enableServiceWorker || ENABLE_SERVICE_WORKER;
	this.options.pdfOptions = this.options.pdfOptions || {
		printBackground: true
	};
	this.options.browserDebuggingPort = this.options.browserDebuggingPort || BROWSER_DEBUGGING_PORT;
	this.options.timeoutStatusCode = this.options.timeoutStatusCode || TIMEOUT_STATUS_CODE;
	this.options.parseShadowDom = this.options.parseShadowDom || PARSE_SHADOW_DOM;
	this.options.enableProxyPool = this.options.enableProxyPool || ENBALE_PROXY_POOL;

	this.browser = require('./browsers/chrome');

	return this;
};



server.start = function() {
	console.log('Starting Prerender');
	this.isBrowserConnected = false;
	this.startPrerender().then(() => {

		process.on('SIGINT', () => {
			this.killBrowser();
			setTimeout(() => {
				console.log('Stopping Prerender');
				process.exit();
			}, 500);
		});

	}).catch(() => {
		if(process.exit) {
			process.exit();
		}
	});
};



server.startPrerender = function() {
	return new Promise((resolve, reject) => {
		this.spawnBrowser().then(() => {

			this.listenForBrowserClose();
			return this.connectToBrowser();
		}).then(() => {
			this.browserRequestsInFlight = new Map();
			this.lastRestart = new Date().getTime();
			this.isBrowserConnected = true;
			console.log(`Started ${this.browser.name}: ${this.browser.version}`);
			return this.firePluginEvent('connectedToBrowser');
		}).then(() => resolve())
		.catch((err) => {
			console.log(err.stack);
			console.log(`Failed to start and/or connect to ${this.browser.name}. Please make sure ${this.browser.name} is running`);
			this.killBrowser();
			reject();
		});
	});
};



server.addRequestToInFlight = function(req) {
	this.browserRequestsInFlight.set(req.prerender.reqId, req.prerender.url);
};



server.removeRequestFromInFlight = function(req) {
	this.browserRequestsInFlight.delete(req.prerender.reqId);
};



server.isAnyRequestInFlight = function() {
	return this.browserRequestsInFlight.size !== 0;
}



server.isThisTheOnlyInFlightRequest = function(req) {
	return this.browserRequestsInFlight.size === 1 && this.browserRequestsInFlight.has(req.prerender.reqId);
}



server.spawnBrowser = function() {

	console.log(`Starting ${this.browser.name}`);
	return this.browser.spawn(this.options);
};



server.killBrowser = function() {
	console.log(`Stopping ${this.browser.name}`);
	this.isBrowserClosing = true;
	this.browser.kill();
};



server.restartBrowser = function() {
	this.isBrowserConnected = false;
	console.log(`Restarting ${this.browser.name}`);
	this.browser.kill();
};



server.connectToBrowser = function() {
	return this.browser.connect();
};



server.listenForBrowserClose = function() {
	let start = new Date().getTime();

	this.isBrowserClosing = false;

	this.browser.onClose(() => {
		this.isBrowserConnected = false;
		if(this.isBrowserClosing) {
			console.log(`Stopped ${this.browser.name}`);
			return;
		}

		console.log(`${this.browser.name} connection closed... restarting ${this.browser.name}`);
		
		if (new Date().getTime() - start < 1000) {
			console.log(`${this.browser.name} died immediately after restart... stopping Prerender`);
			return process.exit(1);
		}

		this.startPrerender();
	});
};



server.waitForBrowserToConnect = function() {
	return new Promise((resolve, reject) => {
		var checks = 0;

		let check = () => {
			if(++checks > 100) {
				return reject(`Timed out waiting for ${this.browser.name} connection`);
			}

			if (!this.isBrowserConnected) {
				return setTimeout(check, 200);
			}

			resolve();
		}

		check();
	});
};


server.use = function(plugin) {
	this.plugins.push(plugin);
	if (typeof plugin.init === 'function') plugin.init(this);
};


server.gainProxyUrl = function(req) {
	return new Promise((resolve) => {
		if (req.prerender.disableProxy) {
			resolve(undefined);
		} else if(req.prerender.proxyUrl) {
			resolve(req.prerender.proxyUrl);
		} else if (this.options.enableProxyPool) {
			resolve(util.gainProxyUrl());
		}

		resolve(undefined);
	})
}


server.onRequest = function(req, res) {

	req.prerender = util.getOptions(req);
	console.log("prerender : " + JSON.stringify(req.prerender))
	// Do not rename reqId!
	req.prerender.reqId = uuidv4();
	req.prerender.renderId = uuidv4();
	req.prerender.start = new Date();
	req.prerender.responseSent = false;
	req.server = this;

	if (!req.prerender.userAgent) {
		req.prerender.userAgent = util.gainUserAgent()
	}
	
	console.log('getting', req.prerender.url);
	if (this.browserRequestsInFlight === undefined) {
		return res.sendStatus(503);
	}
	this.addRequestToInFlight(req);


	this.gainProxyUrl(req)
	.then((proxyUrl) => {
		console.log(`${req.prerender.url} ; proxy : ${proxyUrl} ; userAgent : ${req.prerender.userAgent}`)
		if (proxyUrl) {
			req.prerender.proxyUrl = proxyUrl;
		}
		return this.firePluginEvent('requestReceived', req, res)
	}) 
	// this.firePluginEvent('requestReceived', req, res)
	.then(() => {
		// TODO node 的 express 框架会转发网站的其他请求到这里，但是却是未 join 的 url。比如，fpCollect.min.js
		if (!req.prerender.url.startsWith("http")) {
			// req.prerender.url = new URL
		}
		if (req.prerender.url != 'about:blank' && !validUrl.isWebUri(encodeURI(req.prerender.url))) {
			console.log('invalid URL:', req.prerender.url);
			req.prerender.statusCode = 400;
			return Promise.reject();
		}

		req.prerender.startConnectingToBrowser = new Date();

		return this.firePluginEvent('connectingToBrowserStarted', req, res);
	}).then(() => this.waitForBrowserToConnect())
	.then(() => {
		req.prerender.startOpeningTab = new Date();

		//if there is a case where a page hangs, this will at least let us restart chrome
		setTimeout(() => {
			if (!req.prerender.responseSent) {
				console.log('response not sent for', req.prerender.url);
			}
			this.removeRequestFromInFlight(req);
		}, 60000);

		return this.browser.openTab(req.prerender);

	}).then((tab) => {
		req.prerender.endOpeningTab = new Date();
		req.prerender.tab = tab;

		return this.firePluginEvent('tabCreated', req, res);
	}).then(() => {
		if (req.prerender.url != 'about:blank') {
			req.prerender.startLoadingUrl = new Date();
			return this.browser.loadUrlThenWaitForPageLoadEvent(req.prerender.tab, req.prerender.url,
				() => this.firePluginEvent('tabNavigated', req, res));
		} else if(req.prerender.htmlContent) {
			return this.browser.setDocumentContent(req.prerender.tab, req.prerender.htmlContent);
		}
	}).then(() => {
		req.prerender.endLoadingUrl = new Date();

		if (req.prerender.javascript) {
			return this.browser.executeJavascript(req.prerender.tab, req.prerender.javascript);
		} else {
			return Promise.resolve();
		}
	}).then(() => {
		return this.firePluginEvent('beforeParse', req, res);
	}).then(() => {
		req.prerender.startParse = new Date();

		if (req.prerender.renderType == 'png') {

			return this.browser.captureScreenshot(req.prerender.tab, 'png', req.prerender.fullpage);

		} else if (req.prerender.renderType == 'jpeg') {

			return this.browser.captureScreenshot(req.prerender.tab, 'jpeg', req.prerender.fullpage);

		} else if (req.prerender.renderType == 'pdf') {

			return this.browser.printToPDF(req.prerender.tab, this.options.pdfOptions);

		} else if (req.prerender.renderType == 'har') {

			return this.browser.getHarFile(req.prerender.tab);
		} else {

			return this.browser.parseHtmlFromPage(req.prerender.tab);
		}
	}).then(() => {
		req.prerender.endParse = new Date();

		req.prerender.statusCode = req.prerender.tab.prerender.statusCode;
		req.prerender.prerenderData = req.prerender.tab.prerender.prerenderData;
		req.prerender.content = req.prerender.tab.prerender.content;
		req.prerender.headers = req.prerender.tab.prerender.headers;
		req.prerender.interception = req.prerender.tab.prerender.interception

		return this.firePluginEvent('pageLoaded', req, res);
	}).then(() => {
		this.finish(req, res);
	}).catch((err) => {
		if (err) {
			console.log(err);
			console.log(err.stack);
		}
		req.prerender.startCatchError = new Date();
		this.finish(req, res);
	}).finally(() => {
		this.removeRequestFromInFlight(req);
	});
};



server.finish = function(req, res) {
	req.prerender.startFinish = new Date();

	if (req.prerender.tab) {
		this.browser.closeTab(req.prerender.tab).catch((err) => {
			console.log('error closing Chrome tab', err);
		});
	}

	req.prerender.responseSent = true;
	this.removeRequestFromInFlight(req);

	// if (!this.isAnyRequestInFlight() && new Date().getTime() - this.lastRestart > BROWSER_TRY_RESTART_PERIOD) {
	// 	this.lastRestart = new Date().getTime();
	// 	this.restartBrowser();
	// }

	req.prerender.timeSpentConnectingToBrowser = ((req.prerender.startOpeningTab || req.prerender.startFinish) - req.prerender.startConnectingToBrowser) || 0;
	req.prerender.timeSpentOpeningTab = ((req.prerender.endOpeningTab || req.prerender.startFinish) - req.prerender.startOpeningTab) || 0;
	req.prerender.timeSpentLoadingUrl = ((req.prerender.endLoadingUrl || req.prerender.startFinish) - req.prerender.startLoadingUrl) || 0;
	req.prerender.timeSpentParsingPage = ((req.prerender.endParse || req.prerender.startFinish) - req.prerender.startParse) || 0;
	req.prerender.timeUntilError  = 0;

	if (req.prerender.startCatchError) {
		req.prerender.timeUntilError = req.prerender.startCatchError - req.prerender.start;
	}

	this.firePluginEvent('beforeSend', req, res)
		.then(() => {
			this._send(req, res);
		}).catch(() => {
			this._send(req, res);
		});
};



server.firePluginEvent = function(methodName, req, res) {
	return new Promise((resolve, reject) => {
		let index = 0;
		let done = false;
		let next = null;
		let cancellationToken = null;
		var newRes = {};
		var args = [req, newRes];

		newRes.send = function(statusCode, content) {
			clearTimeout(cancellationToken);
			cancellationToken = null;

			if (statusCode) req.prerender.statusCode = statusCode;
			if (content) req.prerender.content = content;
			done = true;
			reject();
		};

		newRes.setHeader = function(key, value) {
			res.setHeader(key, value);
		}

		next = () => {
			clearTimeout(cancellationToken);
			cancellationToken = null;

			if (done) return;

			let layer = this.plugins[index++];
			if (!layer) {
				return resolve();
			}

			let method = layer[methodName];

			if (method) {
				try {
					cancellationToken = setTimeout(() => {
						console.log(`Plugin event ${methodName} timed out (10s), layer index: ${index}, url: ${req?req.url:'-'}`);
					}, 10000);

					method.apply(layer, args);
				} catch (e) {
					console.log(e.stack);
					next();
				}
			} else {
				next();
			}
		};

		args.push(next);
		next();
	});
};



server._send = function(req, res) {

	req.prerender.statusCode = parseInt(req.prerender.statusCode) || 504;
	let contentTypes = {
		'jpeg': 'image/jpeg',
		'png': 'image/png',
		'pdf': 'application/pdf',
		'har': 'application/json'
	}

	if (req.prerender.renderType == 'html') {
		Object.keys(req.prerender.headers || {}).forEach(function(header) {
			try {
				res.setHeader(header, req.prerender.headers[header].split('\n'));
			} catch (e) {
				console.log('warning: unable to set header:', header);
			}
		});
	}

	if (req.prerender.prerenderData || req.prerender.renderType == 'json') {
		res.setHeader('Content-Type', 'application/json');
	} else {
		res.setHeader('Content-Type', contentTypes[req.prerender.renderType] || 'text/html;charset=UTF-8');
	}

	if (!req.prerender.prerenderData) {
		if (req.prerender.content) {
			if (Buffer.isBuffer(req.prerender.content)) {
				res.setHeader('Content-Length', req.prerender.content.length);
			} else if (typeof req.prerender.content === 'string'){
				res.setHeader('Content-Length', Buffer.byteLength(req.prerender.content, 'utf8'));
			}
		}
	}

	//if the original server had a chunked encoding, we should remove it since we aren't sending a chunked response
	res.removeHeader('Transfer-Encoding');
	//if the original server wanted to keep the connection alive, let's close it
	res.removeHeader('Connection');

	res.removeHeader('Content-Encoding');

	res.status(req.prerender.statusCode);

	let header = '';
	// if (req.prerender.sunflower) {
	// 	header = "url=" + req.prerender.url + "\nfetch_time=" + Math.floor(Date.now() / 1000) + "\n";
	// }

	if (req.prerender.renderType == 'json') {
		let ret = {
			url: req.prerender.url,
			realUrl: req.prerender.realUrl,
			proxy: req.prerender.proxyUrl,
			userAgent: req.prerender.userAgent,
			statusCode: req.prerender.statusCode,
			headers: req.prerender.headers,
			content: header + req.prerender.content
		};
		if (req.prerender.prerenderData) {
			ret['prerenderData'] = req.prerender.prerenderData;
		}
		if (req.prerender.interceptionStr) {
			interceptionsRets = []
			for (const [requestId, interception_entity] of req.prerender.interceptions) {
				interceptionsRets.push(Object.fromEntries(interception_entity));
			}
			ret['interceptions'] = interceptionsRets;
		}
		res.json(ret);
	}

	if (contentTypes[req.prerender.renderType]) {
		res.end(req.prerender.content, 'binary');
	}

	if (!contentTypes[req.prerender.renderType] && !req.prerender.prerenderData && req.prerender.renderType != 'json' && req.prerender.content) {
		res.end(header + req.prerender.content);
	}

	if (!req.prerender.content) {
		res.end();
	}

	var ms = new Date().getTime() - req.prerender.start.getTime();
	console.log('got', req.prerender.statusCode, 'in', ms + 'ms', 'for', req.prerender.url);
};
