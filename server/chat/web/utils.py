from models import ConversationParty, Message

def get_number_of_unread_messages(user_id, conversation_id):
	cp = ConversationParty.select().where((ConversationParty.user==user_id) & (ConversationParty.conversation==conversation_id)).first()
	m = cp.last_read_message
	if m:
		return Message.select().where((Message.conversation==conversation_id) & (Message.ts > m.ts)).count()
	return Message.select().where(Message.conversation==conversation_id).count()