from flask import Blueprint, request
from functools import partial
from db import db, ma
from Models.Users import User, UserSchema 
from Controllers.auth_controller import authorize
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/users')


# return all users in database [admins only]
@users_bp.route('/')
def all_users():

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)

# return user info for logged in user [e.g. view user profile]
@users_bp.route('/profile/')
@jwt_required()
def user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user_info = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(user_info)

# edit user profile [logged in user only]
@users_bp.route('/current/edit_profile/', methods=['PATCH'])
@jwt_required()
def edit_user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user: 
        data = UserSchema().load(request.json, partial=True)
        #users can only edit their name, gender and age
    
        user.name = data['name'],
        user.gender = data['gender'],
        user.age = data['age']
        #commit changes to the database 
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)


#route for user to delete their account 
@users_bp.route('/current/delete_account/', methods=['DELETE'])
@jwt_required()
def delete_account():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message" : "User has been successfully deleted"}


#route for user to delete a users account [i.e. ban them]
@users_bp.route('/<int:id>/delete/', methods=['DELETE'])
@jwt_required(id)
def admin_delete_account():

    #check to see if user is an admin:
    if not authorize():
        return {'error': 'You must be an admin'}, 401

    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message" : "User has been successfully deleted"}




