
module.exports = {
    beforeParse: (req, res, next) => {
        cookies = req.prerender.tab.Network.getCookies()
        .then((obj) => {
            cookies = {}
            obj.cookies.forEach(function(element, index, array) {
                cookies[element.name] = element.value
              })
            req.prerender.tab.prerender.cookies = cookies
        }).catch((error) => console.log(error))
        return next();
    }
}