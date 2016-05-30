from tornado.websocket import WebSocketHandler
from web.helpers import get_from_env
import redis
import gevent
import json
from copy import copy

import pdb

class ChatBackend(object):

	def __init__(self):
		self.chat_channel = get_from_env('chat_channel')
		self.redis = redis.from_url(get_from_env('redis_url'))
		self.pubsub = self.redis.pubsub()
		self.pubsub.subscribe(self.chat_channel)
		self.chat_users = {}

	def __iter_data(self):
		for message in self.pubsub.listen():
			if message.get('type') == 'message':
				yield message.get('data')

	def work(self, message):
		pass

	def start(self):
		gevent.spawn(self.run)

	def run(self):
		for data in self.__iter_data():
			data_decoded = data.decode("utf-8")
			message_json = json.loads(data_decoded)
			message_to_client = copy(message_json)
			del message_to_client['recipient_ids']
			for recipient_id in message_json.get('recipient_ids'):
				# pdb.set_trace()
				user_client = self.chat_users.get(recipient_id,'')
				if user_client:
					gevent.spawn(self.send_message_to_client, user_client, message_to_client)

	def subscribe_user(self, handler):
		if handler and handler.user_id:
			self.chat_users[int(handler.user_id)] = handler
		else:
			raise ValueError('Invalid handler provided')

	def unsubscribe_user(self, handler):
		if handler and handler.user_id:
			del self.chat_users[handler.user_id]
		else:
			raise ValueError('Invalid handler provided')

	def send_message_to_redis(self, message):
		self.redis.publish(self.chat_channel, message)

	def send_message_to_client(self, client, message):
		try:
			client.write_message(message)
		except Exception:
			raise Exception('Couldn\'t send chat message to client')

chat_backend = ChatBackend()
chat_backend.start()