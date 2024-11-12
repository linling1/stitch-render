
module.exports = {
    beforeParse: (req, res, next) => {
        if (req.prerender.tab.prerender.interceptions) {
            console.log('##### interception plugin #####')
            for(const [key, value] of req.prerender.tab.prerender.interceptions) {
                req.prerender.tab.Network.getResponseBody({'requestId':key})
                .then((obj) => {
                    let {body, base64Encoded} = obj;
                    value.set('content', body);
                    // console.log(`url : ${req.prerender.tab.prerender.interception.url} ; statusCode : ${req.prerender.tab.prerender.interception.statusCode} ; headers : ${JSON.stringify(req.prerender.tab.prerender.interception.headers)} ; body : ${body} ; base64Encoded : ${base64Encoded}`);
                }).catch((error) => console.log(error))
            }
            
		}

        return next();
    }
}