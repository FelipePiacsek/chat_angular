from tornado.websocket import WebSocketHandler
from web.messages import save_message, mark_message_as_read
from web.helpers import get_from_env
from web.chat_backend import chat_backend
from flask.ext.security import current_user
import re
import json

class ChatHandler(WebSocketHandler):

	def __init__(self, *args, **kwargs):
		super(ChatHandler, self).__init__(*args, **kwargs)
		self.user_id = None
		self.current_conversation = None

	def check_origin(self, origin):
		return True # change in production

	def open(self, user_id):
		
		if user_id:
			print('Opening chat handler for user ' + user_id)
			self.user_id = user_id
			chat_backend.subscribe_user(self)
		else:
			raise ValueError('Websocket must provide user id on open')

	def on_message(self, message):
		
		message_json = json.loads(message)
		message_type = message_json.get('type', '')
		if message_type == 'mark_as_read':
			mark_message_as_read(user_id=self.user_id,
								 message=message_json)

		elif message_type == 'chat_message':
			m = save_message(self.user_id, message_json)
			chat_backend.send_message_to_redis(m)
		else:
			raise ValueError('Invalid message')

	def on_close(self):
		chat_backend.unsubscribe_user(self)



