#django_tornado
This is just simple example of django running in tornado WSGI container with sockjs-tornado.
<br>
Sample application display current computer time in browser updated each second.
<br>
There is also chat example using django based requests on server side to get data, and tornado-sockjs to send back data to client. 
<br>
Look at views.py cause I use some session trick when serving index.html.
<br>
Chat example is in chat.py file, one line is located in urls.py.

##configuration
Protocol, port and host are in constraint.py file.
<br>
Default settings are http 127.0.0.1 8080

##run
- python django_tornado.py
- go to browser url http://127.0.0.1:8080/

##chat
Simple chat app with memory storage and callbacks when user leaves/joins chat.
<br>
Server side logic is in chat.py and client side in chat.js
<br>
Also since we can add calback to PushClientStore and listen to sockjs client add / remove there is simple "howto" in urls.py
<pre>
PushClientStore.register('chat', chat.ChatStorage.callback)
</pre>

Enjoy ;)
