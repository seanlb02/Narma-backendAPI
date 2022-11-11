
from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from marshmallow import fields
from marshmallow.validate import Length, OneOf, Range

VALID_GENDERS = ('Male', 'Female', 'Non-Binary', 'Other')

class Bot(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String, nullable = False)
    picture = db.Column(db.VARCHAR(1000), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    connections = db.relationship('Connections', back_populates='bot', cascade = "all, delete")
    content = db.relationship('Content', back_populates = 'bot', cascade = "all, delete")


class BotSchema(ma.Schema):

    #validation rules 
    name = fields.String(required=True, validate=Length(min=2))
    bio = fields.String(required=True, validate=Length(min=10))
    gender = fields.String(required=True, validate= OneOf(VALID_GENDERS))
    picture = fields.String(required=True, validate=Length(min=10))
    age = fields.Integer(required=True, validate=Range(min=16, max=99))
    
    class Meta:
        model = Bot
        fields = ('id', 'name', 'bio', 'gender', 'picture', 'age')
        ordered = True

