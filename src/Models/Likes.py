from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields

class Likes(db.Model):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship('User', back_populates = 'likes')
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable = False)
    message = db.relationship('Messages', back_populates = 'likes', cascade = 'all, delete')

class LikesSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password', 'connections'])
    message = fields.Nested('MessagesSchema')

    model = Likes
    fields = ('id', 'user_id', 'message_id', 'user', 'message')
