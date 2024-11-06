#!/usr/bin/env node
var prerender = require('./lib');
const util = require("./lib/util")

util.redefine_log()

process.on('uncaughtException', function(err) {
    console.error('Caught exception: ' + err.stack);
});

var server = prerender();

// server.use(prerender.sendPrerenderHeader());
server.use(prerender.browserForceRestart());
// server.use(prerender.blockResources());
server.use(prerender.addMetaTags());
server.use(prerender.realUrl());
server.use(prerender.sunflower());
server.use(prerender.interceptionUrl());
// server.use(prerender.removeScriptTags());
server.use(prerender.httpHeaders());

server.start();
