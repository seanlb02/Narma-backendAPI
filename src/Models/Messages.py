from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields

class Messages (db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key = True)
    connection_id = db.Column(db.ForeignKey("Connections.id"), nullable = False)
    connection = db.relationship('Connections', back_populates = 'messages')
    content = db.Column(db.Bytea, nullable = False)
    timestamp = 