module.exports = {
    beforeParse: (req, res, next) => {
        if (req.prerender.detail == false) {
            return next();
        }

        req.prerender.tab.Runtime.evaluate({
            expression: `(
                document.querySelectorAll('html, body, body *').forEach((element) => {
                    let style = getComputedStyle(element);
                    if (style.visibility !== 'visible') {
                        return;
                    }
                    console.log(style)
                    let dom_style_info = '';
                    let _to_int = function(property) {
                        if (style[property] === undefined) {
                            return ''
                        }
                        value = style[property];
                        if (/\\d/.test(value) === true) {
                            value = parseInt(value, 10);
                        }
                        return value
                    }
                    
                    let _to_map = function(property, mapping) {
                        if (style[property] != undefined) {
                            if (mapping[style[property].toLowerCase()] != undefined) {
                                return mapping[style[property].toLowerCase()]
                            }
                        }
                        return ''
                    }
                    
                    let _rgb_to_int = function RGBToHex(rgb) {
                        // Choose correct separator
                        let sep = rgb.indexOf(",") > -1 ? "," : " ";
                        // Turn "rgb(r,g,b)" into [r,g,b]
                        rgb = rgb.substr(4).split(")")[0].split(sep);
                        
                        let r = (+rgb[0]).toString(16),
                            g = (+rgb[1]).toString(16),
                            b = (+rgb[2]).toString(16);
                        
                        if (r.length == 1)
                            r = "0" + r;
                        if (g.length == 1)
                            g = "0" + g;
                        if (b.length == 1)
                            b = "0" + b;
                        
                        return parseInt(r + g + b,16);
                    }
                
                    let _zIndex_to_int = function(property) { 
                        if (style[property] == 'auto'){
                            return 0
                        } else {
                            return style[property]
                        };
                    }
                    
                    let displays = {
                        "none" : 1,
                        "block" : 2,
                        "inline-block" : 3,
                        "list-item" : 4,
                        "run-in" : 5,
                        "compact" : 6,
                        "marker" : 7,
                        "table" : 8,
                        "inline-table" : 9,
                        "table-row-group" : 10,
                        "table-header-group" : 11,
                        "table-footer-group" : 12,
                        "table-row" : 13,
                        "table-column-group" : 14,
                        "table-column" : 15,
                        "table-cell" : 16,
                        "table-caption" : 17,
                        "inherit" : 18
                    }
                    
                    let floats = {
                        "none" : 0,
                        "left" : 1,
                        "right" : 2,
                        "inherit" : 3
                    }
                    
                    let overflows = {
                        "visible" : 0,
                        "hidden" : 1,
                        "scroll" : 2,
                        "auto" : 3
                    }
                    
                    let positions = {
                        "static" : 0,
                        "absolute" : 1,
                        "fixed" : 2,
                        "relative" : 3,
                        "inherit" : 4
                    }
                    
                    let text_aligns = {
                        "left": 0,
                        "right": 1,
                        "center": 2,
                        "justify": 3,
                        "inherit" : 4
                    }
                    
                    let properties = {
                        "borderBottomWidth": _to_int,
                        "borderLeftWidth": _to_int,
                        "borderRightWidth": _to_int,
                        "borderTopWidth": _to_int,
                        "fontSize": _to_int,
                        "fontWeight": function(property){return 3 + style[property] / 100;},
                        "paddingBottom": _to_int,
                        "paddingLeft": _to_int,
                        "paddingRight": _to_int,
                        "paddingTop": _to_int,
                        "display": function(property){ return _to_map(property, displays)},
                        "float": function(property){ return _to_map(property, floats)},
                        "overflowX": function(property){ return _to_map(property, overflows)},
                        "overflowY": function(property){ return _to_map(property, overflows)},
                        "position": function(property){ return _to_map(property, positions)},
                        "color": function(property) { return _rgb_to_int(style[property])},
                        "textAlign": function(property){ return _to_map(property, text_aligns)},
                        "textIndent": _to_int,
                        "zIndex": _zIndex_to_int,
                    };
                    
                    let all_properties = ["background","backgroundColor","backgroundImage","backgroundPosition","backgroundRepeat","border","borderBottomColor","borderBottomStyle","borderBottomWidth","borderLeftColor","borderLeftStyle","borderLeftWidth","borderRightColor","borderRightStyle","borderRightWidth","borderTopColor","borderTopStyle","borderTopWidth","opacity","height","width","font","fontSize","fontStyle","fontWeight","listStyle","marginBottom","marginLeft","marginRight","marginTop","paddingBottom","paddingLeft","paddingRight","paddingTop","bottom","left","right","top","clear","display","float","overflowX","overflowY","position","color","lineHeight","textAlign","textIndent","whiteSpace","textOverflow","zIndex"]
                    
                    all_properties.forEach(function(property) {
                        if (properties[property] === undefined) {
                            console.log("not found property : " + property)
                            dom_style_info += ';';
                        } else {
                            value = properties[property](property)
                            console.log("--- found property : " + property + " ; value : " + value)
                            dom_style_info += value + ';';
                        }
                    });
                    let rect = element.getBoundingClientRect();
                    let surface_vision_info = ( Math.floor(rect.width) || 0) + ';' + ( Math.floor(rect.height) || 0) + ';' + ( Math.floor(rect.left) || 0) + ';' + ( Math.floor(rect.top) || 0) + ';' + (style.display === 'none' ? 0 : 1);
                    element.setAttribute('surface_vision_info', surface_vision_info);
                    element.setAttribute('dom_style_info', dom_style_info);
                    if (element.childElementCount == 0 && element.textContent != undefined && element.textContent != '') {
                        let text_vision_info = ( Math.floor(rect.width) || 0) + ';' + ( Math.floor(rect.height) || 0) + ';' + ( Math.floor(rect.x) || 0) + ';' + ( Math.floor(rect.y) || 0) + ';' + element.textContent.split('\\n').length;
                        element.setAttribute('text_vision_info', text_vision_info);
                    }
                }
                )
            )`
        }).then(Promise.resolve());


        return next();
    }
};