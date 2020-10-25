""" Import required modules """
import os
from os.path import join, dirname
from flask import Flask, render_template, request
from dotenv import load_dotenv
import flask_socketio
from flask_sqlalchemy import SQLAlchemy
import models
import chatbot

MESSAGES_RECEIVED_CHANNEL = "messages received"
USER_COUNT = [0]

# Create the Flask application
app = Flask(__name__)

# Initialize socket connection to the flask app
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# Load the keys.env file
dotenv_path = join(dirname(__file__), "keys.env")
load_dotenv(dotenv_path)

# Setup PSQL/SQLAlchemy database connection
database_uri = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
db = SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()


def emit_all_messages(channel):
    """ Persists all usernames, picurls, and messages from database """
    all_user_names = [
        db_users.user_name for db_users in db.session.query(models.ChatHistory).all()
    ]

    all_pic_urls = [
        db_picurl.pic_url for db_picurl in db.session.query(models.ChatHistory).all()
    ]

    all_messages = [
        db_message.message for db_message in db.session.query(models.ChatHistory).all()
    ]

    # Broadcast all messages to all clients
    socketio.emit(
        channel,
        {
            "allUserNames": all_user_names,
            "allPicUrls": all_pic_urls,
            "allMessages": all_messages,
        },
    )


@socketio.on("connect")
def on_connect():
    """ Socket connection """
    print("Someone connected!")
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@socketio.on("disconnect")
def on_disconnect():
    """ Socket disconnection """
    print("Someone disconnected!")


@socketio.on("new google user")
def on_new_google_user(data):
    """ Gather information from user google login authentication """
    user_name = data["name"]
    pic_url = data["picUrl"]
    print("Got an event for new google user input with data: ", data)

    # Broadcast username/profile pic url to all clients
    socketio.emit("userName", {"userName": user_name, "picUrl": pic_url}, request.sid)

    USER_COUNT[0] += 1

    # Broadcast updated usercount to all clients
    socketio.emit("userConnected", {"userCount": USER_COUNT}, broadcast=True)


@socketio.on("new facebook user")
def on_new_facebook_user(data):
    """ Gather information from user facebook login authentication """
    user_name = data["name"]
    pic_url = data["picUrl"]
    print("Got an event for new facebook user input with data: ", data)

    # Broadcast username/profile pic url to all clients
    socketio.emit("userName", {"userName": user_name, "picUrl": pic_url}, request.sid)

    USER_COUNT[0] += 1

    # Broadcast updated usercount to all clients
    socketio.emit("userConnected", {"userCount": USER_COUNT}, broadcast=True)


@socketio.on("logout")
def on_logout():
    """ Decrement user count on logout """
    USER_COUNT[0] -= 1

    # Broadcast updated usercount to all clients
    socketio.emit("userDisconnected", {"userCount": USER_COUNT})


@socketio.on("new message")
def on_new_message(data):
    """ When a new message comes in, store data into database """
    print("Received message: ", data)

    db.session.add(
        models.ChatHistory(data["userName"], data["picUrl"], data["message"])
    )
    db.session.commit()

    # If message starts with '!!' call the bot
    if data["message"][0:2] == "!!":
        captain = chatbot.Bot(data["message"])
        data["message"] = captain.bot_responses()
        data["userName"] = "Captain Bot"
        data["picUrl"] = "https://avatarfiles.alphacoders.com/792/79207.jpg"
        print("Received message from bot: ", data)

        db.session.add(
            models.ChatHistory(data["userName"], data["picUrl"], data["message"])
        )
        db.session.commit()

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@app.route("/")
def index():
    """ Displays the home page accessible at the addresss '/' """
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return render_template("index.html")


# Run the application
if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
        port=int(os.getenv("PORT", 8080)),
        host=os.getenv("IP", "0.0.0.0"),
    )
