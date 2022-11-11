from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields

class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"), nullable = False)
    bot = db.relationship('Bot', back_populates = 'content')
    content = db.Column(db.VARCHAR(1000), nullable = False)
    messages = db.relationship('Messages', back_populates = 'content')

class ContentSchema(ma.Schema):
    bot = fields.Nested('BotSchema', exclude=["id", "bio", "gender", "age"])

    class Meta:
        model = Content
        fields = ('content', 'bot', 'bot_id')
        ordered = True