const {execSync, fork} = require('child_process');
const os = require('os');

function getChromeLocation() {

	let platform = os.platform();

	if (platform === 'darwin') {
		return '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome';
	}

	if (platform === 'linux') {
		return '/chrome-linux/chrome';
	}

	if (platform === 'win32') {
		return 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe';
	}
};


function envClear() {
    let clocation = getChromeLocation()
    let command = `ps aux | grep "${clocation}" | awk '{print $2}' | xargs -I{} kill {}`;
    console.log(command);
    try {
        execSync(command);
    } catch {
        return;
    }
}

function start() {
    envClear();
    // let ChildProcess = fork('./server.js', [], {env: {ENBALE_PROXY_POOL:'true'}});
    let ChildProcess = fork('./server.js');
    ChildProcess.on('exit', function(code) {
        console.log('process exits : ' + code);
        if (code !== 0) {
            setTimeout(start, 1000);
        }
    });
}

start();
