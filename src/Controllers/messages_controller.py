
from os import name
from flask import Blueprint, request
from db import db, ma
from Models.Connections import Connections, ConnectionsSchema   
from Models.Messages import Messages, MessagesSchema
from Models.Content import Content, ContentSchema   
from Controllers.auth_controller import authorize
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime


messages_bp = Blueprint('messages', __name__, url_prefix='/messages')



#route for admins to send messages to each bot's connections/followers
@messages_bp.route('/<int:id>/send/', methods=['POST'])
@jwt_required()
def send_message(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    bot_id = id
    content_id = request.json.get('content_id')
    #select connections the bot is part of
    stmt = db.select(Connections).filter_by(bot_id = bot_id)
    conversations = db.session.scalars(stmt)
    #select a list of content the selected bot has
    stmt2 = db.select(Content).filter_by(id=content_id)
    bot_content = db.session.scalars(stmt2)
    
    # The following logic is a safeguard to ensure bots can only send content that belongs to them 

    if bot_content:
        for i in bot_content:
            if i.bot.id == bot_id:
                if conversations:
                    for i in conversations:
                            messages = Messages(
                                connection_id = i.id,
                                content_id = content_id,
                                timestamp = datetime.now()
                                )
                                #add and commit new messages to db
                            db.session.add(messages)
                            db.session.commit()
                            #respond to client request:
                            return {"success" : "message sent to followers"}
                else:
                        return {"error" : "bot has no followers"}, 204
            else: 
                    return {"error" : "that content doesnt belong to this bot"}

        


#route for admins to get access to all messages from a specific bot
@messages_bp.route('/<int:id>/all/')
@jwt_required()
def show__all_messages(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401
  
    stmt = db.select(Messages).filter(Messages.content.has(bot_id=id))
    message_list = db.session.scalars(stmt)
    if message_list:
        #responds with everything a message needs: id, timestamp, content, bot name, bot photo.
        return MessagesSchema(many=True).dump(message_list)
    else:
        return {"message": "no messages yet"}, 204


#route for logged in users to access their messages from a defined bot
@messages_bp.route('/<string:name>/')
@jwt_required()
def show_messages(name):

    stmt = db.select(Messages).filter(Messages.connection.has(user_id= get_jwt_identity())).filter(Connections.bot.has(name=name))
    message_list = db.session.scalars(stmt)
    if message_list:
        return MessagesSchema(many=True).dump(message_list)
    else:
        return {"message": "no messages yet"}, 204


# route for admins to DELETE messages from a defined bot
@messages_bp.route('/<int:id>/delete/', methods=['DELETE'])
@jwt_required()
def delete_message(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Messages).filter_by(id=id)
    result = db.session.scalar(stmt) 
    if result:
        db.session.delete(result)
        db.session.commit()
        return {'success': 'message has been deleted'}, 200
    else:
        return {'error': 'No message was found to delete'}, 204  
