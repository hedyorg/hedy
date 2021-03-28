# This file is only used on Heroku, to make the integration with nginx work
#
# It makes the server listen on a UNIX socket (where nginx will balance to it)
# and writes a file on startup so nginx knows when the backend is ready to accept
# traffic.
def when_ready(server):
    open('/tmp/app-initialized', 'w').close()

bind = 'unix:///tmp/nginx.socket'
