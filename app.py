# Import required packages
from flask import Flask, render_template
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask_socketio
import flask_sqlalchemy
import models
import random

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

def bot(message):
    if (message[0:2] == '!!'):
        if (message == '!!about' or message == '!! about'):
            db.session.add(models.Chat('This is a pirate themed chat app with many capabilities! Explore away!'))
            db.session.commit()
            
        elif (message == '!!help' or message == '!! help'):
            db.session.add(models.Chat('Here are the known commands you can use: !!about - !!help - !!mood'))
            db.session.commit()
            
        elif (message == '!!mood' or message == '!! mood'):
            moods = ["I'm feeling bored.",
                    "I'm feeling tired.",
                    "I'm feeling naughty.",
                    "I'm feeling sad.",
                    "I'm feeling lazy.",
                    "I'm feeling joyful.",
                    "I'm feeling happy.",
                    "I'm feeling hungry.",
                    "I'm feeling energetic.",
                    "I'm feeling goofy.",
                    "I'm feeling lonely."]
            db.session.add(models.Chat(random.choice(moods)))
            db.session.commit()
            
        else:
            db.session.add(models.Chat('Sorry, I do not recognize that command. Please enter a command starting with "!!"'))
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
    
    db.session.add(models.Chat(data['message']))
    db.session.commit()
    
    bot(data['message'])
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
