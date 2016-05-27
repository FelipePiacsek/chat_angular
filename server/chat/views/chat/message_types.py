
COMMON_TEXT_MAX_LEN = 20

def common_text(args):
	text = args.get('text', '')
	return text, (text[:COMMON_TEXT_MAX_LEN] + '...') if len(text) > COMMON_TEXT_MAX_LEN else text