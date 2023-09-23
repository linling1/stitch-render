const {fork} = require('child_process');
const util = require("./lib/util")




function start() {
    util.killChrome();
    let ChildProcess = fork('./server.js', [], {env: {ENBALE_PROXY_POOL:'true'}});
    // let ChildProcess = fork('./server.js');
    ChildProcess.on('exit', function(code) {
        console.log('process exits : ' + code);
        if (code !== 0) {
            setTimeout(start, 1000);
        }
    });

    setTimeout(()=> ChildProcess.kill("SIGKILL"), 600000)
}

start();

