from models import Conversation, ConversationParty, ConversationType, Photo, User, database
from web.helpers import datetime_to_string
from web.photos import get_user_photo
from web.users import get_user_data
from peewee import fn

def update_conversation(conversation_id, last_message=None):
	
	Conversation.update(last_message=last_message).where(Conversation.id==conversation_id).execute()


def create_conversation(conversation):

	conversation_type = conversation.get('conversation_type')
	ct = ConversationType.get(ConversationType.name == conversation_type)

	c = Conversation()
	c.conversation_type = ct

	picture = None
	p_url = conversation.get('picture','')

	if p_url:
		picture = Photo()
		picture.url = p_url

	name = conversation.get('name','')
	
	cps = []

	conversationees_list = conversation.get('conversationees_list')
	conversationees_list = list(set(conversation.get('conversationees_list',[])))


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

	return __jsonify_one_conversation(c)


def get_conversation_json(user_id=None, conversation_id=None):
	
	if conversation_id:
		conversations = Conversation.select().where(Conversation.id == conversation_id).first()
	elif user_id:
		conversations = Conversation.select().join(ConversationParty,on=Conversation.id==ConversationParty.conversation).where(ConversationParty.user==user_id)
	else:
		conversations = None
	return __jsonify_conversations(conversations)
		

def __jsonify_conversations(conversations):

		if conversations:
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
	c['last_message'] = lm

	return c