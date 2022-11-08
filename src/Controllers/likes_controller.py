
from os import name
from flask import Blueprint, request
from db import db, ma
from Models.Connections import Connections, ConnectionsSchema
from Models.Messages import Messages, MessagesSchema   
from Models.Likes import Likes, LikesSchema
from sqlalchemy import or_

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


likes_bp= Blueprint("Likes", __name__, url_prefix='/likes')


#route for logged in user to like a message
@likes_bp.route('/message/like/', methods=['POST'])
@jwt_required()
def like_message():
    message_id = request.json.get("message_id")
    user = get_jwt_identity()

    stmt = db.select(Likes).filter_by(user_id=user).filter_by(message_id=message_id)
    liked = db.session.scalar(stmt)

    #user can only like a message once
    if not liked:
        likes = Likes(
            user_id = user,
            message_id = message_id
            )
        #add new like to the database
        db.session.add(likes)
        db.session.commit()
        #return message to client
        return {"message" : f"message {message_id} was liked by user {user}"}
    
    if liked:
        return {"message" : 'You are not allowed to like a message twice!'}

#route for user to unlike a message

@likes_bp.route('/message/unlike/', methods=['DELETE'])
@jwt_required()
def unlike_message():
    message = request.json.get("message_id")
    user = get_jwt_identity()
    stmt = db.select(Likes).filter_by(message_id = message)
    like = db.session.scalar(stmt)

    if like:
        db.session.delete(like)
        db.session.commit()
        return {'success' : f'message {message} was unliked by user {user}'} 


# route to return a count of like for a given message
@likes_bp.route('/message/<int:id>/total/')
def message_total_likes(id):
    stmt = db.select(db.func.count()).select_from(Likes).filter_by(message_id = id)
    count = db.session.scalar(stmt)

    if count <= 1:
        return {'Message Likes' : f'{count}'}
    else:
        return {'error' : 'This message has no likes yet'}



# route to return messages a user a liked 
@likes_bp.route('/user/total/')
@jwt_required()
def user_likes():
    user = get_jwt_identity()
    stmt = db.select(Likes).filter_by(user_id=user)
    likes = db.session.scalars(stmt)

    if likes:
        return LikesSchema(many=True).dump(likes)



