from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from marshmallow import fields 
from marshmallow.validate import Length, Range, Email, OneOf, And, Regexp


VALID_GENDERS = ('Male', 'Female', 'Non-binary', 'Other')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    email = db.Column(db.String, nullable = False) 
    password = db.Column(db.String, nullable = False)
    gender = db.Column(db.String())
    age = db.Column(db.Integer)
    connections = db.relationship('Connections', back_populates='user', cascade = "all, delete")
    likes = db.relationship('Likes', back_populates='user', cascade = "all, delete")

class UserSchema(ma.Schema):
    connections = fields.List(fields.Nested('ConnectionsSchema', exclude=['user']))
    likes = fields.List(fields.Nested('LikesSchema', exclude=['user']))

    #validation rules
    name = fields.String(required=True, validate=Length(min=2))
    email = fields.String(required=True, validate=Length(min=10))
    password = fields.String(required=True, validate=And(Length(min=8), Regexp('^[a-zA-Z0-9]')))
    gender = fields.String(required=True, validate= OneOf(VALID_GENDERS))
    age = fields.Integer(required=True, validate=Range(min=16, max=99))


    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'gender', 'age', 'connections')
        ordered = True