from flask import Blueprint, request
from functools import partial
from db import db, ma
from Models.Users import User, UserSchema 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/users')


# return all users in database [admins only]
@users_bp.route('/')
def all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)

# return user info for logged in user [e.g. view user profile]
@users_bp.route('/profile/')
@jwt_required()
def user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user_info = db.session.scalars(stmt)
    return UserSchema(many=True).dump(user_info)

# edit user profile [logged in user only]
@users_bp.route('/edit_profile/', methods=['PATCH'])
@jwt_required()
def edit_user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user: 
        data = UserSchema().load(request.json, partial=True)
        #users can only edit their name, gender and age
        
        user.name = data['name'],
        # user.email = user.email,
        # user.password = user.password,
        user.gender = data['gender'],
        user.age = data['age']
        #commit changes to the database 
        db.session.commit()
        return UserSchema().dump(user)
    else: 
        return {"error": "User session expired, please log in again"}, 404

