from models import Conversation, ConversationParty, database
from web.helpers import datetime_to_string
from peewee import fn

def get_conversation_json(conversation_id=None):
	if conversation_id:
		conversations = Conversation.select().where(Conversation.id == conversation_id).first()
	else:
		conversations = Conversation.select()
	return __jsonify_conversations(conversations)
	

def __jsonify_conversations(conversations):

		if conversations:
			q = ConversationParty.select(ConversationParty.conversation, fn.Max(ConversationParty.last_message_ts)).group_by(ConversationParty.conversation)
			if hasattr(conversations, '__iter__'):
				json_list = []
				for conversation in conversations:
					cp = ConversationParty.select().where(ConversationParty.conversation == conversation.id).first()
					json_list.append(__jsonify_one_conversation(conversation, cp))
				return json_list
			else:
				cp = ConversationParty.select().where(ConversationParty.conversation == conversations.id).first()
				return __jsonify_one_conversation(conversations, cp)
		return None
					

def __jsonify_one_conversation(conversation, conversation_party):

	c = dict()
	lm = dict()

	lm['date'] = datetime_to_string(conversation_party.last_message_ts) if conversation_party and conversation_party.last_message_ts else ''
	lm['text'] = conversation_party.last_message if conversation_party and conversation_party.last_message else ''

	c['id'] = conversation.id if conversation else ''
	c['name'] = conversation.name if conversation and conversation.name else ''
	c['last_message'] = lm

	return c