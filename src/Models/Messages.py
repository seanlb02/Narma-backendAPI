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
    content = db.Column(db.VARCHAR(length=2000), nullable = False)
    timestamp = db.Column(db.DateTime)
    likes = db.relationship('Likes', back_populates = 'message')

class MessagesSchema(ma.Schema):
    connection = fields.Nested('ConnectionsSchema')

    content = fields.String(required=True, validate=Length(min=2))

    class Meta:
        model = Messages
        fields = ('id', 'content', 'timestamp', 'connection.id')
        