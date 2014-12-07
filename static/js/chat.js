/**
 * Created with IntelliJ IDEA.
 * User: michal@vane.pl
 * Date: 07.12.14
 * Time: 14:59
 * To change this template use File | Settings | File Templates.
 */

var chat;
(function(chat) {
    chat.enterKeyDownHandler = function(event) {
        var keyCode = (window.event) ? e.which : e.keyCode;
        if(keyCode == 13) {
            RequestEnter();
        }
    }

    chat.enterHandler = function(event) {
        RequestEnter();
    }

    chat.messageKeyDownHandler = function(event) {
        var keyCode = (window.event) ? e.which : e.keyCode;
        if(keyCode == 13) {
            RequestPost();
        }
    }

    chat.messageHandler = function(event) {
        RequestPost();
    }

    chat.request = {}

    RequestPost = function() {
        var data = {};
        data['msg'] = fx.id("chat_msg_txt").value;
        data['csrfmiddlewaretoken'] = fx.Const.CSRF;
        return $.ajax({
            type:"POST",
            dataType:"json",
            data:data,
            url:'/chat/msg/',
            success: function(data) {
                if(Validate(data)) {
                    fx.id("chat_msg_txt").value = "";
                }
                console.log(data)
            },
            error:function(data) {
                fx.debug(data.responseText);
            }
        });
    }

     function RequestEnter() {
        var data = {};
        data['nick'] = fx.id("chat_enter_txt").value;
        data['csrfmiddlewaretoken'] = fx.Const.CSRF;
        return $.ajax({
            type:"POST",
            dataType:"json",
            data:data,
            url:'/chat/enter/',
            success: function(data) {
                if(Validate(data)) {
                    fx.id("chat_enter_div").style.display = "none";
                    fx.id("chat_container_div").style.display = "inline";
                    fx.id("chat_msg_txt").focus();
                }
                console.log(data)
            },
            error:function(data) {
                fx.debug(data.responseText);
            }
        });
    }

    function Validate(data) {
        return data.type == 'res' && data.data == 'OK';
    }

    chat.dataCallback = function(o) {
        if(o.type == "test") {
            var d = new Date(o.data);
            fx.html("date_span", fx.dateFull(d));
        } else {
            console.log(o);
            if(o.type == 'ch_usr') {
                var d = o.data;
                var out = "";
                for(var i = 0;i<d.length;i++) {
                    out += d[i]+"<br>";
                }
                fx.html('chat_usr_div', out);
            } else if(o.type == 'ch_last_msg'){
                var data = o.data;
                var out = "";
                for(var i = 0;i<data.length;i++) {
                    var d = data[i];
                    out += ""+fx.dateTime(new Date(d.date)) + " " + d.usr + " : " + d.msg+"<br>";
                }
                fx.htmla('chat_msg_div', out);
            } else if(o.type == 'ch_usr_del'){
                var html = fx.id('chat_usr_div').innerHTML;
                html = html.replace(o.data+"<br>", "");
                fx.html('chat_usr_div', html);
                fx.htmla('chat_msg_div', "<b>User "+o.data+" left chat</b><br>");
            } else if(o.type == 'ch_usr_new'){
                fx.htmla('chat_usr_div', o.data+"<br>")
                fx.htmla('chat_msg_div', "<b>User "+o.data+" joined chat</b><br>");
            } else if(o.type == 'ch_msg'){
                var d = o.data;
                var msg = ""+fx.dateTime(new Date(d.date)) + " " + d.usr + " : " + d.msg+"<br>";
                fx.htmla('chat_msg_div', msg);
            }
            fx.scrollBottom('chat_msg_div');
            fx.scrollBottom('chat_usr_div');
            fx.id("chat_msg_txt").focus();
        }
    }

})(chat || (chat = {}));