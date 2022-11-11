from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields
from datetime import datetime
from marshmallow.validate import Length


class Messages (db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key = True)
    connection_id = db.Column(db.Integer, db.ForeignKey("connections.id"), nullable = False)
    connection = db.relationship('Connections', back_populates = 'messages')
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"), nullable = False)
    content = db.relationship('Content', back_populates = 'messages')
    timestamp = db.Column(db.DateTime)
    likes = db.relationship('Likes', back_populates = 'message', cascade = "all, delete") 

class MessagesSchema(ma.Schema):
    connection = fields.Nested('ConnectionsSchema')
    content = fields.Nested('ContentSchema')

    class Meta:
        model = Messages
        fields = ('id', 'timestamp', 'connection.id', 'content')
        ordered = True
        