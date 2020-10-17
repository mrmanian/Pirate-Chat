import flask_sqlalchemy
from app import db

# PSQL/SQLAlchemy database model
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120))
    picUrl = db.Column(db.String(600))
    message = db.Column(db.String(10485760))
    
    def __init__(self, userName, picUrl, message):
        self.userName = userName
        self.picUrl = picUrl
        self.message = message
        
    def __repr__(self):
        return '<userName: {}\npicUrl: {}\nmessage: {}'.format(self.userName, self.picUrl, self.message)
