
from os import name
from flask import Blueprint, request
from db import db, ma
from Models.Connections import Connections, ConnectionsSchema   
from Models.Messages import Messages, MessagesSchema
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

#route for admins to upload messages to a bot's connection
#i.e. user can 

# @messages_bp.route('/<string:name>/add', methods=['POST'])
# @jwt_required()
# def send_message(name):

    





#route for logged in users to access their messages from a defined bot
@messages_bp.route('/<string:name>/')
@jwt_required()
def show_messages(name):
    stmt = db.select(Messages).filter_by(Connections.user.has(user_id= get_jwt_identity())).filter(Connections.bot.has(name=name))
    message_list = db.session.scalars(stmt)
    return MessagesSchema(many=True).dump(message_list)