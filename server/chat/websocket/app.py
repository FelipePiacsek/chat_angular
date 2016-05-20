from tornado.options import define, options
import tornado.ioloop
import tornado.web
from websocket.websocket import ChatHandler
import os

def start_websocket_app():

	define('port',default=os.environ.get(config.get('chat_websocket_port')))

	app = tornado.web.Application([
		(r'/'+os.environ.get(confi.get('chat_uri')), ChatHandler),
	])

	app.listen(options.port)

	tornado.ioloop.IOLoop.instance().start()

	return app