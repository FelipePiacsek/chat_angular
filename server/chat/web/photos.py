from models import Photo, ConversationParty, database

def get_user_photo(index, conversationees_list):
	if not len(conversationees_list) == 2:
		return None
	picture = ConversationParty.select(ConversationParty.picture).where(ConversationParty.user==conversationees_list[index-1]).first()
	return picture.id