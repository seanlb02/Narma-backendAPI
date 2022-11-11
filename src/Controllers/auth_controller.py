from flask import Blueprint, request
from db import db, ma, bcrypt 
from Models.Bot import Bot, BotSchema   
from datetime import timedelta
from Models.Users import User, UserSchema 
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def authorize():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    return user.is_admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



#route to create a user account
@auth_bp.route('/register/', methods=['POST'])
def auth_register():

    data = UserSchema().load(request.json, partial=True)
    user = User(
        name = data['name'],
        email = data['email'],
        password = bcrypt.generate_password_hash(data['password']).decode('utf8'),
        phonenumber=data['phonenumber'],
        gender = data['gender'],
        age = data['age']
    )
    #Add and commit to the database
    db.session.add(user)
    db.session.commit()
    #respond to client request
    return UserSchema().dump(user), 201


#route for registered user to login/ be authenticated with a token
@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    #Locate the user account
    stmt = db.select(User).filter_by(email=request.json.get('email'))
    #store the selected entry into a variable
    user = db.session.scalar(stmt)

    #if user exists and password is correct
    if bcrypt.check_password_hash(user.password, request.json.get('password')):
        #then provide them with a token
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        #and respond to client request with user email, token and auth status(optional-if admin)
        return {'name' : user.name, 'token': token} 
    else:
        return {"error" : "Invalid email or password"}, 401

