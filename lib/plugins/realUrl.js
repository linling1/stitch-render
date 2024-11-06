module.exports = {
    beforeParse: (req, res, next) => {
        req.prerender.tab.Runtime.evaluate({
            expression: `window.location.href`
        })
        .then(realUrl => req.prerender.realUrl=realUrl?.result?.value)
        .then(Promise.resolve());

        return next();
    }
};