from tornado.websocket import WebSocketHandler
from websocket.helpers import save_message

class ChatHandler(WebSocketHandler):
    
	def open(self):
		print('ChatHandler opened')

	def on_message(self, message):
		if message:
			type_name = message.type_name if message.type_name else None
			args = message.args if message.args else None
			file = message.file if message.file else None
			if not type_name or not args:
				error_msg = 'Invalid message with values \n typename:\t{} \n args:\t{}'.format(type_name, args)
				raise ValueError(error_msg) 
			m = save_message(type_name, args, file)
			# send_message_to_redis(m) if m else return

	def on_close(self):
		pass



