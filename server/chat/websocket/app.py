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


tr = WSGIContainer(chat_app)

define('port',default=get_from_env('server_port'))

app = tornado.web.Application([
	(r'/'+get_from_env('chat_uri'), ChatHandler),
	(r'.*', FallbackHandler, dict(fallback=tr))
])

app.listen(options.port)

IOLoop.instance().start()