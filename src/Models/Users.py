from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from marshmallow import fields 


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    email = db.Column(db.String, nullable = False) 
    password = db.Column(db.String, nullable = False)
    gender = db.Column(db.String())
    age = db.Column(db.Integer)
    connections = db.relationship('Connections', back_populates='user', cascade = "all, delete")

class UserSchema(ma.Schema):
    connections = fields.List(fields.Nested('ConnectionsSchema', exclude=['user']))
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'gender', 'age', 'connections')
        ordered = True