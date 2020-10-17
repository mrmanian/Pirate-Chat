# Import required packages
from flask import Flask, render_template, request
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask_socketio
import flask_sqlalchemy
import models
import random
import requests
import chatbot

# Sets channel for messages received
MESSAGES_RECEIVED_CHANNEL = 'messages received'

# Create the Flask application
app = Flask(__name__)

# Initialize socket connection to the flask app
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

# Load the sql.env file
dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

# Setup PSQL/SQLAlchemy database connection
database_uri = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

# Global variables
userCount = 0
userName = 'Pirate '
            
# Persists all usernames, picurls, and messages from database
def emit_all_messages(channel):
    all_usernames = [ \
    db_users.userName for db_users in \
        db.session.query(models.ChatHistory).all()]
        
    all_picurls = [ \
    db_picurl.picUrl for db_picurl in \
        db.session.query(models.ChatHistory).all()]
        
    all_messages = [ \
    db_message.message for db_message in \
        db.session.query(models.ChatHistory).all()]
        
    # Broadcast all messages to all clients
    socketio.emit(channel, {
        'allUserNames': all_usernames,
        'allPicUrls': all_picurls,
        'allMessages': all_messages
    })
    
# On new connection
@socketio.on('connect')
def on_connect():
    global userCount
    global userName
    randNum = str(random.randint(0, 99999))
    userCount += 1
    name = userName + randNum
    print('Someone connected!')
    
    # Broadcast updated usercount to all clients
    socketio.emit('userConnected', {
        'userCount': userCount
    }, broadcast = True)
    
    # Broadcast assigned username to all clients
    socketio.emit('userName', {
        'userName': name
    }, request.sid)
    
    print('Assigned name: ' + name)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
# On disconnection
@socketio.on('disconnect')
def on_disconnect():
    global userCount
    userCount -= 1
    print ('Someone disconnected!')
    
    # Broadcast updated usercount to all clients
    socketio.emit('userDisconnected', {
        'userCount': userCount
    })
    
# When a new message comes in
@socketio.on('new message')
def on_new_message(data):
    print('Received message: ', data)
    
    # Stores data into database
    db.session.add(models.ChatHistory(data['userName'], '', data['message']))
    db.session.commit()
    
    # If message starts with '!!' call the bot 
    if data['message'][0:2] == '!!':
        captain = chatbot.Bot(data['message'])
        data['message'] = captain.botResponses()
        data['userName'] = 'Captain Bot'
        fullMessage = data['userName'] + ': ' + data['message']
        print('Received message from bot: ', data)
        
        db.session.add(models.ChatHistory(data['userName'], '', data['message']))
        db.session.commit()
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
# Displays the home page accessible at the addresss '/'
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
