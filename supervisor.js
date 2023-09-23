const {fork, execSync} = require('child_process');
const util = require("./lib/util")


function killChildProcess() {
    console.log("===== Kill Server =====");
    let command = `ps aux | grep "node ./server.js" | awk '{print $2}' | xargs -I{} kill -9 {}`;
    console.log(command);
    try {
        execSync(command);
    } catch {
        return;
    }
}


function start(first) {
    util.killChrome();
    console.log("########## START SERVER ##########")
    let ChildProcess = fork('./server.js', [], {env: {ENBALE_PROXY_POOL:'true'}});
    // let ChildProcess = fork('./server.js');
    ChildProcess.on('exit', function(code) {
        console.log('process exits : ' + code);
        if (code !== 0) {
            setTimeout(start, 1000);
        }
        console.log("cycle restart server")
        setTimeout(()=> killChildProcess(), 600000);
        
    });

    if(first) {
        console.log("first to cycle restart server")
        setTimeout(()=> killChildProcess(), 600000);
    }
    
}

start(true);
