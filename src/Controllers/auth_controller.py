from flask import Blueprint, request
from db import db, ma, bcrypt
from Models.Bot import Bot, BotSchema   
from datetime import timedelta
from Models.Users import User, UserSchema 
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required



auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


#route to create a user account
@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try: 
        #create a new model instance from user info
        user = User(
            name = request.json.get('name'),
            email = request.json.get('email'),
            password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf8'),
            gender = request.json.get('gender'),
            age = request.json.get('age')
        )
        db.session.add(user)
        db.session.commit()
        #respond to client request
        return UserSchema().dump(user), 201
    except ValueError:
        return {'error': 'Please fill in all the required fields'}, 400
    except IntegrityError:
        return {"error" : "email already in use"}

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

