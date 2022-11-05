
from os import name
from flask import Blueprint, request
from db import db, ma
from Models.Connections import Connections, ConnectionsSchema   
from Models.Messages import Messages, MessagesSchema
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime


messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

#route for admins to upload messages to each bot's connections/followers
@messages_bp.route('/<int:id>/send/', methods=['POST'])
@jwt_required()
def send_message(id):
    #select connections the bot is part of
    bot_id = id
    stmt = db.select(Connections).filter_by(bot_id = bot_id)
    conversations = db.session.scalars(stmt)
    
    # return(ConnectionsSchema(many=True).dump(conversations))
    if conversations:
        # for i in conversations:
        #     messages = Messages(
        #         connection_id = i.id,
        #         content = "test message2",
        #         timestamp = datetime.now()
        #         )
        #         #add and commit new messages to db
        #     db.session.add(messages)
        #     db.session.commit()
        # #respond to client request:
        return {"success" : "Messages have been sent"}
    else:
        return {"error" : "bot has no followers"}, 204



#route for logged in users to access their messages from a defined bot
@messages_bp.route('/<int:id>/')
@jwt_required()
def show_messages(id):
    stmt = db.select(Messages).filter(Messages.connection.has(user_id= get_jwt_identity())).filter(Connections.bot.has(id=id))
    message_list = db.session.scalars(stmt)
    if message_list:
        return MessagesSchema(many=True).dump(message_list)
    else:
        return {"message": "no messages yet"}, 204