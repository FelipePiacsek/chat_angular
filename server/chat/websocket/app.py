from tornado.options import define, options
from websocket.websocket import ChatHandler
from web.config import config
from web.helpers import get_from_env
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.web import FallbackHandler
from tornado.httpserver import HTTPServer
from app import app as chat_app
import tornado.web
import os


http_server = HTTPServer(WSGIContainer(chat_app))
http_server.listen(get_from_env('server_port'))

# tr = WSGIContainer(chat_app)

define('port',default=get_from_env('chat_websocket_port'))

app = tornado.web.Application([
	(r'/'+get_from_env('chat_uri'), ChatHandler)
])

app.listen(options.port)

IOLoop.instance().start()