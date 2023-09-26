const adblockRust = require('adblock-rs');
const fs = require('fs');
const dataPath = './lib/adblock/data/'

const debugInfo = true;
const filterSet = new adblockRust.FilterSet(debugInfo);

const easylistFilters = fs.readFileSync(
    dataPath + 'easylist.to/easylist/easylist.txt',
    { encoding: 'utf-8' },
).split('\n');
filterSet.addFilters(easylistFilters);

const uboUnbreakFilters = fs.readFileSync(
    dataPath + 'uBlockOrigin/unbreak.txt',
    { encoding: 'utf-8' },
).split('\n');
filterSet.addFilters(uboUnbreakFilters);

const resources = adblockRust.uBlockResources(
    dataPath + 'test/fake-uBO-files/web_accessible_resources',
    dataPath + 'test/fake-uBO-files/redirect-resources.js',
    dataPath + 'test/fake-uBO-files/scriptlets.js'
);

const engine = new adblockRust.Engine(filterSet, true);
engine.useResources(resources);

exports.AdBlockEngine = engine;