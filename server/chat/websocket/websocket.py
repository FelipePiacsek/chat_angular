from tornado.websocket import WebSocketHandler
from web.messages import save_message
from web.helpers import get_from_env
from web.chat_backend import chat_backend
from flask.ext.security import current_user
import re
import json

class ChatHandler(WebSocketHandler):

	def __init__(self, *args, **kwargs):
		super(ChatHandler, self).__init__(*args, **kwargs)
		self.user_id = None

	def check_origin(self, origin):
		return True # change in production

	def open(self):
		if not current_user:
			raise ValueError
		print('Opening chat handler for user ' + current_user.id)
		if user_id:
			self.user_id = current_user.id
			chat_backend.subscribe_user(self)
		else:
			raise ValueError('Websocket must provide user id on open')

	def on_message(self, message):
		if message:
			message_json = json.loads(message)
			m = save_message(self.user_id, message_json)
			chat_backend.send_message_to_redis(m)
		else:
			raise ValueError('Received null message')

	def on_close(self):
		chat_backend.unsubscribe_user(self)



