#!/usr/bin/env node
var prerender = require('./lib');

var server = prerender();

// server.use(prerender.sendPrerenderHeader());
server.use(prerender.browserForceRestart());
// server.use(prerender.blockResources());
server.use(prerender.addMetaTags());
server.use(prerender.sunflower());
server.use(prerender.interceptionUrl());
// server.use(prerender.removeScriptTags());
server.use(prerender.httpHeaders());

server.start();
