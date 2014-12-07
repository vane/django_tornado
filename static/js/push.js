/**
 * Created with IntelliJ IDEA.
 * User: michal@vane.pl
 * Date: 16.11.14
 * Time: 03:01
 * To change this template use File | Settings | File Templates.
 */

var ph;

(function(ph) {
    ph.URL = null;
    ph.RECONNECT_TIMEOUT = 5000;
    ph.callbacks = []
    ph.start = function() {
        console.log("START");
        console.log(ph.URL);
        var sock = new SockJS(ph.URL);

        var s = function send(data) {
            console.log("sockjs send : "+data);
            sock.send(data);
        }
        sock.onopen = function () {
            console.log("sockjs open");
        }
        var i = 0;
        sock.onmessage = function(e) {
            //console.log("sockjs message");
            var o = JSON.parse(e.data);
            for(i = 0;i<ph.callbacks.length;i++) {
                ph.callbacks[i].call(null, o);
            }
        }

        sock.onclose = function() {
            console.log("sockjs close");
            setTimeout("ph.start()", ph.RECONNECT_TIMEOUT);
        }
    }
    ph.register = function(callback) {
        ph.callbacks.push(callback)
    }
})(ph || (ph = {}));
