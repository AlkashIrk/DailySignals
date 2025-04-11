import secrets

from flask import Flask
from flask_socketio import SocketIO

from flask_app.settings.messages import init_messages
from flask_app.settings.routes import init_views
from flask_app.settings.template_filters import init_filters

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(128)
print("secret: " + app.config['SECRET_KEY'])

socketio = SocketIO(app)
init_views(app)
init_filters(app)
init_messages(socketio)


def run_flask():
    host_name = "0.0.0.0"
    port = 5010
    socketio.run(app, debug=True, use_reloader=False, port=port, host=host_name)
