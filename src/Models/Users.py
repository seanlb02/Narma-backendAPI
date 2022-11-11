from operator import is_
from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from marshmallow import fields, validates, ValidationError 
from marshmallow.validate import Length, Range, Email, OneOf, And, Regexp
from datetime import datetime, date, timedelta
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

VALID_GENDERS = ('Male', 'Female', 'Non-binary', 'Other')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String, nullable = False, unique = True) 
    password = db.Column(db.String, nullable = False, unique = True)
    phonenumber = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    age = db.Column(db.Date, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = True, default = False)
    connections = db.relationship('Connections', back_populates='user', cascade = "all, delete")
    likes = db.relationship('Likes', back_populates='user', cascade = "all, delete")

class UserSchema(ma.Schema):
    connections = fields.List(fields.Nested('ConnectionsSchema', exclude=['user']))
    likes = fields.List(fields.Nested('LikesSchema', exclude=['user']))

    #validation rules
    name = fields.String(required=True, validate=Length(min=2))
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True, validate=And(Length(min=8), Regexp('^[a-zA-Z0-9]')))
    phonenumber = fields.String(required=True)
    gender = fields.String(required=True, validate= OneOf(VALID_GENDERS))
    age = fields.Date(required=True)
    is_admin = fields.Boolean(default=False)

    #conditional validator for user age:
    @validates('age')
    def validate_age(self, birthdate): 
        age = (date.today() - birthdate) // timedelta(days=365.2425)
        if age < 16:
            raise ValidationError("User is too young to register")
        
    #3rd party phone number validator:
    @validates('phonenumber')
    def validate_phonenumber(self, phonenumber):
        check = carrier._is_mobile(number_type(phonenumbers.parse(phonenumber)))
        if check is False:
            raise ValidationError("Phone number is not valid")

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'phonenumber', 'gender', 'age', 'connections')
        ordered = True