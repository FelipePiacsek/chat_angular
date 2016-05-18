from flask import Flask
from datetime import datetime

app = Flask(__name__)

app.run()

# endpoints

app.route('/conversations')
def get_conversations_tab_info():
	cp = list(ConversationParty.select().dicts())
	return json.dumps({'conversations':cp})


app.route('/conversation/<conversation_id>')
def get_conversation_tab_info(conversation_id):

	cp = ConversationParty.select().join(Conversation, on=Conversation.id==ConversationParty.conversation).where(ConversationParty.conversation==conversation_id).first()

	if cp:
		return _new_conversation_tab_info(cp.conversation.id,
		cp.user.avatar,
		cp.user.get_name(),
		cp.last_message_ts,
		cp.last_message)
	else:
		return _new_conversation_tab_info(None,
		None,
		None,
		None,
		None)


@app.route('/conversation_data/<conversation_id>')
def get_conversation_data(conversation_id):
	cps = ConversationParty.select().where(ConversationParty.conversation==conversation_id)
	messages = list(Messages.select().where(Message.conversation_party << cps).dicts())
	return _new_message_data(messages)


# supporting methods

def _new_conversation_tab_info(conversation_id,
							   picture,
							   name,
							   datetime,
							   text):
	return {
		'conversation_id': conversation_id if conversation_id else '',
		'last_conversationee': {'picture': picture if picture else '', 'name': name if name else ''},
		'last_message': {'date': datetime if datetime else '', 'text': text if text else ''}
	}

def _new_message_data(messages):
	return {
		'messages': messages if messages else []
	}

app.run()