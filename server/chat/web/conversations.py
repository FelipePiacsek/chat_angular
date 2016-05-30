from models import Conversation, ConversationParty, ConversationType, Photo, User, database
from web.helpers import datetime_to_string
from web.photos import get_user_photo
from web.users import get_user_data
from web.chat_config import config as conversations_config
from views.chat.exceptions import InvalidConversationException
from peewee import fn

def update_conversation(conversation_id, last_message=None):
	
	Conversation.update(last_message=last_message).where(Conversation.id==conversation_id).execute()


def create_conversation(user_id, conversation):

	conversation_type = conversation.get('conversation_type')
	ct = ConversationType.get(ConversationType.name == conversation_type)

	conversationees_list = conversation.get('conversationees_list')
	conversationees_list = list(set(conversation.get('conversationees_list',[])))

	if conversation_type == conversations_config.get('CONVERSATION_DIRECT_TYPE') and len(conversationees_list) != 2:
		raise InvalidConversationException('Direct conversation should have 2 conversationees')

	c = Conversation()
	c.conversation_type = ct

	picture = None
	p_url = conversation.get('picture','')

	if p_url:
		picture = Photo()
		picture.url = p_url

	name = conversation.get('name','')
	
	cps = []

	for index, conversationee in enumerate(conversationees_list):
		
		n, p = name, picture if conversation_type == 'group' else get_user_data(index, conversatinees_list)

		cp = ConversationParty()
		cp.conversation = c
		cp.name = n 
		cp.user = User.get(User.id==conversationee)
		cp.picture = p
		cps.append(cp)


	with database.transaction():
		c.save()
		if picture:
			picture.save()
		for cp in cps:
			cp.save()

	return __jsonify_one_conversation(user_id, c)


def get_conversation_json(user_id, conversation_id=None):
	
	if conversation_id and user_id:
		conversations = Conversation.select().where(Conversation.id == conversation_id).first()
	elif user_id:
		conversations = Conversation.select().join(ConversationParty,on=Conversation.id==ConversationParty.conversation).where(ConversationParty.user==user_id)
	else:
		conversations = None
	return __jsonify_conversations(user_id, conversations)
		

def __jsonify_conversations(user_id, conversations):

		if conversations:
			if hasattr(conversations, '__iter__'):
				json_list = []
				for conversation in conversations:
					json_list.append(__jsonify_one_conversation(user_id, conversation))
				return json_list
			else:
				return __jsonify_one_conversation(user_id, conversations)
		return None
					

def __jsonify_one_conversation(user_id, conversation):

	cp = ConversationParty.select().where((ConversationParty.conversation == conversation) and (ConversationParty.user == user_id)).first()

	c = dict()
	lm = dict()

	lm['date'] = datetime_to_string(conversation.last_message.ts) if conversation and conversation.last_message else ''
	lm['text'] = conversation.last_message.display_content if conversation.last_message else ''

	c['id'] = conversation.id if conversation else ''
	c['last_message'] = lm
	c['name'] = cp.name if cp and cp.name else ''

	return c