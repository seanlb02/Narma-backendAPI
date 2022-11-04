from db import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from marshmallow import fields

class Likes(db.Model):
    __tablename__ = 'Likes'

    