from tornado.websocket import WebSocketHandler
from web.messages import save_message, mark_message_as_read
from web.helpers import get_from_env
from web.chat_backend import chat_backend
from web.chat_config import config as chat_config
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
			self.user_id = user_id
			print('Opening chat handler for user ' + self.user_id)
			chat_backend.subscribe_user(self)
		else:
			raise ValueError('Websocket must provide user id on open')

	def on_message(self, message):
		
		try:
			message_json = json.loads(message)
			message_data = message_json.get('data')
			message_type = message_json.get('type', '')
			if message_type == chat_config.get('MESSAGE_MARK_AS_READ_TYPE'): 
				mark_message_as_read(user_id=self.user_id,
									 message=message_data.get('message_id'))

			elif message_type == chat_config.get('MESSAGE_CHAT_TYPE'):
				m = save_message(self.user_id, message_data)
				chat_backend.send_message_to_redis(m)
		
		except InvalidMessageDataException as e:
			print(e)
		
		except Exception as e:
			print(e)

	def on_close(self):
		print('Closing chat handler for user ' + self.user_id)
		chat_backend.unsubscribe_user(self)



