from models import Conversation, ConversationParty, ConversationType, Photo, User, database
from web.helpers import datetime_to_string
import web.messages
from web.photos import get_user_photo
from web.users import get_user_data
from web.chat_config import config as conversations_config
from views.chat.exceptions import InvalidConversationException
from peewee import fn, SelectQuery

def update_conversation(conversation_id, last_message=None):
	
	Conversation.update(last_message=last_message).where(Conversation.id==conversation_id).execute()


def create_conversation(user_id, conversation):

	conversation_type = conversation.get('conversation_type')
	conversationees_list = conversation.get('conversationees_list')
	conversationees_list = list(set(conversation.get('conversationees_list',[])))

	if conversation_type == conversations_config.get('CONVERSATION_DIRECT_TYPE') and len(conversationees_list) != 2:
		raise InvalidConversationException('Direct conversations should have 2 conversationees')

	ct = ConversationType.get(ConversationType.name == conversation_type)
	c = Conversation()
	c.conversation_type = ct

	p_url = conversation.get('picture','')
	picture = None
	if p_url:
		picture = Photo()
		picture.url = p_url

	name = conversation.get('name','')
	
	cps = []
	
	myself = None

	for index, conversationee in enumerate(conversationees_list):
		
		n = None
		p = None

		if conversation_type == 'group':
			n = name
			p = picture
		else:
			data = get_user_data(index, conversationees_list)
			n = data[0]
			p = data[1]

		cp = ConversationParty()
		cp.conversation = c
		cp.name = n 
		cp.user = User.get(User.id==conversationee)
		cp.picture = p
		cps.append(cp)

		if conversationee == user_id:
			myself = cp


	with database.transaction():
		c.save()
		if picture:
			picture.save()
		for cp in cps:
			cp.save()

	return __jsonify_one_conversation(myself)


def get_conversation_json(user_id=None, conversation_id=None, conversation_party=None):
	
	if conversation_id and user_id:
		cps = ConversationParty.select().where((ConversationParty.conversation == conversation_id) & (ConversationParty.user == user_id)).first()
	elif user_id:
		cps = ConversationParty.select().where(ConversationParty.user==user_id)
	elif conversation_party:
		cps = conversation_party
	return __jsonify_conversations(cps)
		

def __jsonify_conversations(conversation_parties):

		if conversation_parties:
			if hasattr(conversation_parties, '__iter__') or isinstance(conversation_parties, SelectQuery):
				json_list = []
				for cp in conversation_parties:
					json_list.append(__jsonify_one_conversation(cp))
				return json_list
			else:
				return __jsonify_one_conversation(conversation_parties)
		return None
					

def __jsonify_one_conversation(conversation_party):

	c = dict()
	lm = dict()
	s = dict()

	s['id'] = conversation_party.user.id if conversation_party.user else ''
	s['name'] = conversation_party.user.get_name() if conversation_party.user else ''

	lm['ts'] = datetime_to_string(conversation_party.conversation.last_message.ts) if conversation_party and conversation_party.conversation and conversation_party.conversation.last_message else ''
	lm['text'] = conversation_party.conversation.last_message.display_content if conversation_party and conversation_party.conversation and conversation_party.conversation.last_message else ''
	lm['sender'] = s

	c['id'] = conversation_party.conversation.id if conversation_party and conversation_party.conversation else ''
	c['last_message'] = lm
	c['sender'] = s
	c['name'] = conversation_party.name if conversation_party and conversation_party.name else ''
	c['number_of_unread_messages'] = web.messages.get_number_of_unread_messages(conversation_party.user.id, conversation_party.conversation.id)

	return c