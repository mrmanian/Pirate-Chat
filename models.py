"""Import required modules"""
from app import db


class ChatHistory(db.Model):
    """ PSQL/SQLAlchemy database model """

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120))
    pic_url = db.Column(db.String(600))
    message = db.Column(db.String(10485760))

    def __init__(self, user_name, pic_url, message):
        self.user_name = user_name
        self.pic_url = pic_url
        self.message = message

    def __repr__(self):
        return "<user_name: {}\npic_url: {}\nmessage: {}".format(
            self.user_name, self.pic_url, self.message
        )
