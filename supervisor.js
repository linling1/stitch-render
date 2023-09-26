const {fork, execSync} = require('child_process');
const util = require("./lib/util")



function killChildProcess() {
    console.log(`===== ${new Date().toISOString()} Kill Server =====`);
    let command = `ps aux | grep "node ./server.js" | awk '{print $2}' | xargs -I{} kill -9 {}`;
    console.log(command);
    try {
        execSync(command);
    } catch {
        return;
    }
    // controller.abort();
}


function start(first) {
    util.killChrome();
    console.log(`########## ${new Date().toISOString()} START SERVER ##########`)
    // const controller = new AbortController();
    // const { signal } = controller;
    let ChildProcess = fork('./server.js', [], {env: {ENBALE_PROXY_POOL:'true'}});
    // let ChildProcess = fork('./server.js');
    ChildProcess.on('exit', function(code, signal) {
        console.log(`process exit. code : ${code} ; signal : ${signal}`);
        if (code !== 0) {
            setTimeout(start, 1000);
        }
        console.log("cycle restart server")
        setTimeout(()=> killChildProcess(), 60*60*1000);
        
    });

    ChildProcess.on('error', function(error){
        console.log(`child process error: ${error}`)
    });
    

    if(first) {
        console.log("first to cycle restart server")
        setTimeout(()=> killChildProcess(), 60*60*1000);
    }

    console.log(`ChildProcess pid : ${ChildProcess.pid}`)
    
}



start(true);
