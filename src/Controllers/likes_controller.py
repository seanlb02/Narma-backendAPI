
from os import name
from flask import Blueprint, request
from db import db, ma
from Models.Connections import Connections, ConnectionsSchema   
from sqlalchemy import or_

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


likes_bp= Blueprint("Likes", __name__, url_prefix='/likes')



# route to return a count of message likes
@likes_bp.route('/<string:message_id')

