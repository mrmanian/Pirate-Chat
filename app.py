# Import required packages
from flask import Flask, render_template
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask_socketio
import flask_sqlalchemy
import models 

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def emit_all_messages(channel):
    all_messages = [ \
    db_message.message for db_message in \
        db.session.query(models.Chat).all()]
    
    socketio.emit(channel, {
        'allMessages': all_messages
    })

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new message')
def on_new_message(data):
    print('Received message from someone: ', data)
    
    db.session.add(models.Chat(data['message']));
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    return render_template('index.html')
    
# Run the application
if __name__ == '__main__':
    socketio.run(
        app,
        debug = True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
    )
