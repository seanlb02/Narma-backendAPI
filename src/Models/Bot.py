
from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship



class Bot(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bio = db.Column(db.Text)
    gender = db.Column(db.String)
    connections = db.relationship('Connections', back_populates='bot', cascade = "all, delete")

class BotSchema(ma.Schema):
    class Meta:
        model = Bot
        fields = ('id', 'name', 'bio', 'gender')
        ordered = True

