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

# Chat Bot function 
def bot(message):
    # Only run funtion if message begins with '!!'
    if (message[0:2] == '!!'):
        
        # Bot outputs about message
        if (message == '!!about' or message == '!! about'):
            db.session.add(models.Chat('Captain Bot: This is a pirate themed chat app with many capabilities! Explore away!'))
            db.session.commit()
            
        # Bot outputs help message showing known commands 
        elif (message == '!!help' or message == '!! help'):
            db.session.add(models.Chat('Captain Bot: Here are the known commands you can use: !!about - !!help - !!pirate - !!mood - !!famous - !!funtranslate <message> - !!insult'))
            db.session.commit()
            
        # Bot outputs definition of a pirate (got from urban dictionary)
        elif (message == '!!pirate' or message == '!! pirate'):
            db.session.add(models.Chat('Captain Bot: A guy who drives a ship and yells "yo dude gimme your money and stuff" and gets whatever he wants. Usually has a stash or rum for some reason.'))
            db.session.commit()
            
        # Bot outputs a random mood
        elif (message == '!!mood' or message == '!! mood'):
            moods = ["Captain Bot: I be feelin' like crackin' Jenny's tea cup.",
                    "Captain Bot: I be feelin' ho.",
                    "Captain Bot: I be feelin' marooned.",
                    "Captain Bot: I be feelin' like committin piracy.",
                    "Captain Bot: I be feelin' like taking a caulk.",
                    "Captain Bot: I be feelin' angry.",
                    "Captain Bot: I be feelin' like givin' no quarter.",
                    "Captain Bot: I be feelin' like bringin' a spring upon her cable.",
                    "Captain Bot: I be feelin' to blow the man down.",
                    "Captain Bot: I be feelin' like parleying.",
                    "Captain Bot: I be feelin' like drinkin' a simple grog."]
            db.session.add(models.Chat(random.choice(moods)))
            db.session.commit()
        
        # Bot outputs a random famous pirate
        elif (message == '!!famous' or message == '!! famous'):
            famousPirates = ['Captain Bot: Anne Bonny was a famous pirate.',
                            'Captain Bot: Bartholomew Roberts was a famous pirate.',
                            'Captain Bot: Benjamin Hornigold was a famous pirate.',
                            'Captain Bot: Blackbeard was a famous pirate.',
                            'Captain Bot: Calico Jack was a famous pirate.',
                            'Captain Bot: Charles Vane was a famous pirate.',
                            'Captain Bot: Cheung Po Tsai was a famous pirate.',
                            'Captain Bot: Edward England was a famous pirate.',
                            'Captain Bot: Edward Low was a famous pirate.',
                            'Captain Bot: Grace OMalley was a famous pirate.',
                            'Captain Bot: Henry Every was a famous pirate.',
                            'Captain Bot: Howell Davis was a famous pirate.',
                            'Captain Bot: Mary Read was a famous pirate.',
                            'Captain Bot: Paulsgrave Williams was a famous pirate.',
                            'Captain Bot: Samuel Bellamy was a famous pirate.',
                            'Captain Bot: Stede Bonnet was a famous pirate.',
                            'Captain Bot: Thomas Tew was a famous pirate.',
                            'Captain Bot: Turgut Reis was a famous pirate.',
                            'Captain Bot: William Kidd was a famous pirate.',
                            'Captain Bot: Sayyida al Hurra was a famous pirate.',
                            'Captain Bot: Emanuel Wynn was a famous pirate.',
                            'Captain Bot: Peter Easton was a famous pirate.',
                            'Captain Bot: Richard Worley was a famous pirate.',
                            'Captain Bot: Ching Shih was a famous pirate.',
                            'Captain Bot: Christopher Contend was a famous pirate.',
                            'Captain Bot: Christopher Moody was a famous pirate.']
            db.session.add(models.Chat(random.choice(famousPirates)))
            db.session.commit()
            
        # Bot translates any phrase you want into pirate lingo via API call
        elif (message.split()[0] == '!!funtranslate' or [message[i: i + 15] for i in range(0, len(message), 15)][0] == '!! funtranslate'):
            phrase = message[15:]
            api_link1 = f'https://api.funtranslations.com/translate/pirate.json?text={phrase}'
            parse_data1 = requests.get(api_link1).json()
            print(parse_data1)
            if 'success' in parse_data1:
                translation = 'Captain Bot: '+ parse_data1['contents']['translated']
                db.session.add(models.Chat(translation))
                db.session.commit()
            else:
                db.session.add(models.Chat('Captain Bot: Too Many Requests: Rate limit of 5 requests per hour exceeded.'))
                db.session.commit()
            
        # Bot displays a random pirate insult via API call
        elif (message == '!!insult' or message == '!! insult'):
            api_link2 = 'https://api.fungenerators.com/pirate/generate/insult?limit=5'
            parse_data2 = requests.get(api_link2).json()
            print(parse_data2)
            if 'success' in parse_data2:
                insults = parse_data2['contents']['taunts']
                db.session.add(models.Chat('Captain Bot: ' + random.choice(insults)))
                db.session.commit()
            else:
                db.session.add(models.Chat('Captain Bot: Too Many Requests: Rate limit of 5 requests per day exceeded.'))
                db.session.commit()
        
        # If unknown command, display this
        else:
            db.session.add(models.Chat('Captain Bot: Sorry, I do not recognize that command. Please enter "!!help" to see a list of commands.'))
            db.session.commit()
            
# Persists all messages from database
def emit_all_messages(channel):
    global userName
    all_messages = [ \
    db_message.message for db_message in \
        db.session.query(models.Chat).all()]
        
    # Broadcast all messages to all clients
    socketio.emit(channel, {
        'allMessages': all_messages,
        'userName': userName
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
    
    # Add username and message into one string
    fullMessage = data['userName'] + ': ' + data['message']
    
    # Stores full message into database
    db.session.add(models.Chat(fullMessage))
    db.session.commit()
    
    bot(data['message'])
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
