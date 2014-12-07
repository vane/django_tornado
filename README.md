#django_tornado
This is just simple example of django running in tornado WSGI container with sockjs-tornado
should display current computer time in browser updated each second when running

##configuration
protocol, port and host are in constraint.py file
default are http 127.0.0.1 8080

##run
python django_tornado.py
go to browser url http://127.0.0.1:8080/

and you should see the time
