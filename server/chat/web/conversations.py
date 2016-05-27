from models import Conversation, ConversationParty, database
from web.helpers import datetime_to_string
from peewee import fn

def update_conversation(conversation_id, last_message=None, name=None)
	
	Conversation.update(last_message=last_message,
						name=name)
				.where(Conversation.id==conversation_id)
				.execute()


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
					json_list.append(__jsonify_one_conversation(conversation))
				return json_list
			else:
				return __jsonify_one_conversation(conversations)
		return None
					

def __jsonify_one_conversation(conversation):

	c = dict()
	lm = dict()

	lm['date'] = datetime_to_string(conversation.last_message.ts) if conversation and conversation.last_message else ''
	lm['text'] = conversation.last_message.display_content if conversation.last_message else ''

	c['id'] = conversation.id if conversation else ''
	c['name'] = conversation.name if conversation and conversation.name else ''
	c['last_message'] = lm

	return c