
module.exports = {
    beforeParse: (req, res, next) => {
        if (req.prerender.tab.prerender.interception.hasOwnProperty("requestId") && req.prerender.tab.prerender.interception.requestId) {
            console.log('##### interception plugin #####')
            req.prerender.tab.Network.getResponseBody({'requestId':req.prerender.tab.prerender.interception.requestId})
            .then((obj) => {
				let {body, base64Encoded} = obj;
				req.prerender.tab.prerender.interception.resp = body;
				// console.log(`url : ${req.prerender.tab.prerender.interception.url} ; statusCode : ${req.prerender.tab.prerender.interception.statusCode} ; headers : ${JSON.stringify(req.prerender.tab.prerender.interception.headers)} ; body : ${body} ; base64Encoded : ${base64Encoded}`);
            }).catch((error) => console.log(error))
		}

        return next();
    }
}