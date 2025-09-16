from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()

# ⚡ أضف message_queue هنا
socketio = SocketIO(cors_allowed_origins="*", message_queue="redis://localhost:6379")  

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    socketio.init_app(app)  # لا حاجة لإعادة تحديد cors_allowed_origins هنا

    return app
