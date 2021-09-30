from . import db  
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default= func.now())   #func get current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #Foreign Key link the note with respect to the users.. name small case



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')    # list store all of the notes user owns Name capital