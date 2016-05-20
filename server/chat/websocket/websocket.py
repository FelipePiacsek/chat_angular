from tornado.websocket import WebSocketHandler
from websocket.helpers import save_message



class ChatHandler(WebSocketHandler):
    
	def open(self):
		pass

	def on_message(self, type_name, args, file=None):
		m = save_message(type_name, args, file)
		# send_message_to_redis(m) if m else return

	def on_close(self):
		pass



