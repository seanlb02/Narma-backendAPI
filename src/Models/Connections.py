from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields



class Connections(db.Model):
    __tablename__ = 'connections'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship('User', back_populates = 'connections')
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"), nullable = False)
    bot = db.relationship('Bot', back_populates = 'connections')
    


class ConnectionsSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password', 'connections'])
    bot = fields.Nested('BotSchema')

    class Meta:
        model = Connections
        fields = ('id', 'user', 'bot')
        ordered = True 

