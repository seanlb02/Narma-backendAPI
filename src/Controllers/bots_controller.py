from flask import Blueprint, request
from db import db, ma
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
        return {'error': 'No such bot exists with that gender'}
   
# route for a logged in user to follow a bot after searching by name
@bots_bp.route('/<string:name>/follow', methods = ['POST'])
@jwt_required()
def follow_bot(name):
    stmt = db.select(Bot).filter_by(name=name)
    bot = db.session.scalar(stmt)
    jsonbot = BotSchema(many=True).dump(bot)
    print(bot)
    #fetch bot id (Connections FK) to create new Connections instance directly:
    bot_id = jsonbot.id 
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
        return {"success" : f"you are now connected with {bot_name}"}
    else:
        return {"error" : "You are already connected"}

#route to retrieve bots by gender
# @bots_bp.route('/<name>/')
# def bot_by_gender(name):
#     stmt = db.select(Bot).filter_by(name=name)
#     bot = db.session.scalar(stmt)
#     if bot:
#         return BotSchema().dump(bot)
#     else: 
#         return {'error': 'No such bot exists with that name'}

#route to add new bot to database
@bots_bp.route('/', methods=['POST'])
@jwt_required()
def create_bot():
    bot = Bot(
        name = request.json["name"],
        bio = request.json["bio"], 
        gender = request.json["gender"],
    )

    #Add and Commit to database
    db.session.add(bot)
    db.session.commit()
    #Respond to client request
    return BotSchema().dump(bot), 201

#route to edit an existing bot in database
@bots_bp.route('/<int:id>/', methods=['PATCH'])
def update_one_bot(id):
    stmt = db.select(Bot).filter_by(id=id)
    bot = db.session.scalar(stmt)
    if bot:
        bot.name = request.json.get("name") or bot.name
        bot.bio = request.json.get("bio") or bot.bio
        bot.gender = request.json.get("gender") or bot.gender
        db.session.add(bot)
        db.session.commit()
        return BotSchema().dump(bot)
    else:
        return {'error': 'No such bot exists with that id'}, 404


#route to delete a bot from database
@bots_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required
def delete_one_bot(id):
    stmt = db.select(Bot).filter_by(id=id)
    bot = db.session.scalar(stmt)
    if bot:
        db.session.delete(bot)
        db.session.commit()
        return {'message': 'Bot deleted successfully'}, 200
    else:
        return {'error': 'No such bot exists with that id'}, 404    
