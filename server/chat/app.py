from flask import Flask
from views.chat.blueprint import chat

app = Flask(__name__)
app.register_blueprint(chat)
