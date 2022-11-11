from functools import partial
from flask import Blueprint, request
from db import db, ma
from Controllers.auth_controller import authorize 
from Models.Bot import Bot, BotSchema   
from Models.Connections import Connections, ConnectionsSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity



bots_bp = Blueprint('bots', __name__, url_prefix='/bots')

#route to retrive list of all bots 
@bots_bp.route('/')
def all_bots():
    
    stmt = db.select(Bot)
    bots = db.session.scalars(stmt)
    return BotSchema(many=True).dump(bots)


#route to retrieve a single bot by id
@bots_bp.route('/<int:id>/')
def bot_by_id(id):
    stmt = db.select(Bot).filter_by(id=id)
    bot = db.session.scalar(stmt)
    if bot:
        return BotSchema().dump(bot)
    else: 
        return {"error": "Bot not found"}
    

#route to retrieve a single bot by name 
@bots_bp.route('/<string:name>/')
def bot_by_name(name):
    stmt = db.select(Bot).filter_by(name=name)
    bot = db.session.scalars(stmt)
    if bot:
        return BotSchema(many=True).dump(bot)
    else: 
        return {'error': 'No such bot exists with that name'}
   


#route for admins to add new bot to database
@bots_bp.route('/add/', methods=['POST'])
@jwt_required()
def create_bot():
    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    data = BotSchema().load(request.json)
    bot = Bot(
        name = data["name"],
        bio = data["bio"], 
        gender = data["gender"],
        picture = data["picture"],
        age = data["age"]
    )

    #Add and Commit to database
    db.session.add(bot)
    db.session.commit()
    #Respond to client request
    return BotSchema().dump(bot), 201

#route to edit an existing bot in database [admin only]
@bots_bp.route('/<string:name>/edit/', methods=['PATCH'])
def update_one_bot(name):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Bot).filter_by(name=name)
    bot = db.session.scalar(stmt)

    data = BotSchema().load(request.json, partial=partial)

    if bot:
        bot.name = data["name"] or bot.name
        bot.bio = data["bio"] or bot.bio
        bot.gender = data["gender"] or bot.gender
        bot.age = data["age"] or bot.age
      
        db.session.commit()
        return BotSchema().dump(bot)
    else:
        return {'error': 'No such bot exists with that id'}, 404


#route to delete a bot from database [admin only]
@bots_bp.route('/<int:id>/delete/', methods=['DELETE'])
@jwt_required()
def delete_one_bot(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Bot).filter_by(id=id)
    bot = db.session.scalar(stmt)
    if bot:
        db.session.delete(bot)
        db.session.commit()
        return {'message': 'Bot deleted successfully'}, 200
    else:
        return {'error': 'No such bot exists with that id'}, 404    
