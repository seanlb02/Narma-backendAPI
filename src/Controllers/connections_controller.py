
from os import name
from flask import Blueprint, request, abort
from db import db, ma
from Controllers.auth_controller import authorize
from Models.Connections import Connections, ConnectionsSchema   
from sqlalchemy import or_

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

connections_bp= Blueprint('connections', __name__, url_prefix='/connections')


#route to return all connections [admin only]
@connections_bp.route('/all_connections/')
def all_connections():

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Connections)
    connections = db.session.scalars(stmt)
    return ConnectionsSchema(many=True).dump(connections) 

# route to return a logged in users connections (note: JWT identifier is user_id)
@connections_bp.route('/following/')
@jwt_required()
def user_connections():
    stmt = db.select(Connections).filter_by(user_id = get_jwt_identity())
    connections = db.session.scalars(stmt)
    return ConnectionsSchema(many=True).dump(connections)



#route to add a new connection (i.e. user follows a bot)
@connections_bp.route('/follow/', methods=['POST'])
@jwt_required()
def create_connection():
    bot_id = request.json["bot_id"]
    stmt = db.select(Connections).filter_by(user_id = get_jwt_identity(), bot_id=bot_id)
    exists = db.session.scalar(stmt)
    
    #users can only follow a bot once... 
    if not exists:
        connections = Connections(
        user_id = get_jwt_identity(),
        bot_id = request.json.get("bot_id")
        )

        db.session.add(connections)
        db.session.commit() 
        return {"success" : f"User is now connected with bot {bot_id}"}
    else:
        return {"error" : "User already connected"}


#route to delete a connection from database, [i.e. user unfollows a bot]
@connections_bp.route('/unfollow/', methods=['DELETE'])
@jwt_required()
def unfollow_bot():
    bot_name = request.json["bot_name"]
    stmt = db.select(Connections).filter(Connections.bot.has(name=bot_name)).filter_by(user_id = get_jwt_identity())
    connection = db.session.scalar(stmt)

    if connection:
        db.session.delete(connection)
        db.session.commit()
        return {'message': f'User is no longer connected with {bot_name}'}
    else:
        return {"error" : "No such connection ever existed between these two"}

        