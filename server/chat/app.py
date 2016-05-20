from flask import Flask
from views.chat.blueprint import chat
from websocket.app import start_websocket_app

app = Flask(__name__)
app.register_blueprint(chat)
app.run(debug=True)

start_websocket_app()