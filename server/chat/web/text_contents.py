from models import TextContent, database
from views.chat.message_types import common_text

def save_text_content(args):
	t = common_text(args)
	with database.transaction():
		content = TextContent()
		content.text = t.get('text', '')
		content.save()
		return content