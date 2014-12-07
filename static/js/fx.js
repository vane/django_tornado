/**
 * Created with IntelliJ IDEA.
 * User: michal@vane.pl
 * Date: 07.12.14
 * Time: 14:58
 * To change this template use File | Settings | File Templates.
 */


var fx;
(function(fx) {
    fx.debug = function(data) {
        fx.htmla("debug", data+"<br>");
    }
    fx.log = function(data) {
        console.log(data);
    }
    fx.do = function(func, args) {
        func.call(null, args);
    }
    fx.each = function(data, callback) {
        if(data instanceof Array) {
            for(var i = 0;i< data.length;i++){
                callback.call(null, data[i], i)
            }
        } else {
            var i = 0;
            for(var key in data) {
                i+=1;
                callback.call(null, data[key], i);
            }
        }
        return {done:function(func, args){func.call(null, args)}};
    }
    fx.id = function(data) {
        return document.getElementById(data);
    }
    fx.html = function(name, html) {
        fx.id(name).innerHTML = html;
    }
    fx.htmla = function(name, html) {
        fx.id(name).innerHTML += html;
    }
    fx.htmlp = function(name, html) {
        var e = fx.id(name);
        e.innerHTML = html+ e.innerHTML;
    }

    fx.dateFull = function(d, ds) {
        ds = ds != null ? ds : "/";
        var out = (d.getDate() > 9 ? d.getDate() : "0"+ d.getDate())+ds;
        out += (d.getMonth() > 9 ? d.getMonth() : "0"+ d.getMonth())+ds+d.getFullYear()+" ";
        out += (d.getHours() > 9 ? d.getHours() : "0"+ d.getHours())+":";
        out += (d.getMinutes() > 9 ? d.getMinutes() : "0"+ d.getMinutes())+":";
        out += d.getSeconds() > 9 ? d.getSeconds() : "0"+ d.getSeconds();
        return out;
    }

    fx.dateTime = function(d) {
        var out = (d.getHours() > 9 ? d.getHours() : "0"+ d.getHours())+":";
        out += (d.getMinutes() > 9 ? d.getMinutes() : "0"+ d.getMinutes())+":";
        out += d.getSeconds() > 9 ? d.getSeconds() : "0"+ d.getSeconds();
        return out;
    }

    fx.scrollBottom = function(name) {
        var e = fx.id(name);
        e.scrollTop = e.scrollHeight;
    }

    fx.Const = {
        CSRF:"",
        WIDTH:0,
        HEIGHT:0
    };
})(fx || (fx = {}));