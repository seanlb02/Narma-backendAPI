from flask import Blueprint, request
from db import db, ma, bcrypt 
from Models.Bot import Bot, BotSchema   
from datetime import timedelta
from Models.Content import Content, ContentSchema
from Models.Bot import Bot, BotSchema
from Controllers.auth_controller import authorize 
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

content_bp = Blueprint('content', __name__, url_prefix='/content')

#route for admins to return all content for a specific bot
@content_bp.route('/<string:name>/all/')
@jwt_required()
def bot_content(name):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Content).filter(Content.bot.has(name=name))
    content = db.session.scalars(stmt)

    if content: 
        return ContentSchema(many=True).dump(content)
    else: 
        return  {"message": "no content yet"}, 204


# route for admins to return a specific piece of content via ID
@content_bp.route('/<int:id>/')
@jwt_required()
def fetch_content(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalars(stmt)
    return ContentSchema(many=True).dump(content)


# route for admins to to add new content 
@content_bp.route('/<int:id>/add/', methods=['POST'])
@jwt_required()
def add_content(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    data = ContentSchema().load(request.json)
    content = Content(
        bot_id = data["bot_id"],
        content = data["content"],
        
    )

    #Add and Commit to database
    db.session.add(content)
    db.session.commit()
    #Respond to client request
    return {"message": "Content uploaded successfully"}


# route for admins to edit content 
@content_bp.route('/<int:id>/edit/', methods=['PATCH'])
@jwt_required()
def edit_content(id):

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401
    
    stmt = db.select(Content).filter_by(id=id)
    content = db.session.scalar(stmt)

    data = ContentSchema().load(request.json)

    if content:
        content.bot_id = data["bot_id"] or content.bot_bio
        content.content = data["content"] or content.content
        db.session.commit()
        return {"message": "Content updated successfully"}
    else:
        return {'error': 'No such bot exists with that id'}, 404
