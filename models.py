import flask_sqlalchemy
from app import db

# PSQL/SQLAlchemy database model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(10485760))
    
    def __init__(self, a):
        self.message = a
        
    def __repr__(self):
        return '<Chat message: %s>' % self.message 
