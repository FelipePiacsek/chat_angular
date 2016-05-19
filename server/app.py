from flask import Flask
from views.chat_blueprint import chat

app = Flask(__name__)
app.register_blueprint(chat)
app.run(debug=True)