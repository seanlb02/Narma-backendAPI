import os
from Controllers.bots_controller import bots_bp
from Controllers.users_controller import users_bp
from Controllers.auth_controller import auth_bp
from Controllers.connections_controller import connections_bp
from Controllers.messages_controller import messages_bp
from Controllers.likes_controller import likes_bp
from Models.Bot import Bot
from Models.Users import User
from Models.Connections import Connections
from Models.Messages import Messages
from Models.Likes import Likes
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from db import db, ma, bcrypt, jwt 
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    #app-wide error handler
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error" : err.messages}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(401)
    def unauthorised(err):
        return{'error' : err.messages}, 401
    
    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error' : f'The field {err} is required.'}, 400



    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #register the blueprints/controllers
    app.register_blueprint(bots_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(connections_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(likes_bp)

    @app.cli.command('drop')
    def drop_db():
        db.drop_all()
        print('Tables dropped')
     
    @app.cli.command('create')
    def create_db():
        db.create_all()
        print('Tables created')

    @app.cli.command('seed')
    def seed_db():
        bots = [
            Bot(
                name='John',
                bio='Hey, im john. I love everything fitness!',
                gender='Male',
                picture='empty',
                age = '37'
            ),
            Bot(
                name='Mary',
                bio='Hey, im mary. I love everything fitness!',
                gender='Female',
                picture='empty',
                age = '29'
            )
        
        ]

        db.session.add_all(bots)
        db.session.commit()

        users = [
            User(
                name='Peter',
                email='peter@hotmail.com',
                password='password',
                gender='Male',
                age='25',

            ),
            User(
                name='Debbie',
                email='deb@hotmail.com',
                password='password1',
                gender='Non-binary',
                age='20',
            ),
            User(
                name='Jeremih',
                email='jerryj@gmail.com',
                password='password666',
                gender='Other',
                age='19',
            )
        ]

        db.session.add_all(users)
        db.session.commit()
        

        connections = [
            Connections(
                user = users[0],
                bot = bots[1]
            ), 
            Connections(
                user = users[2],
                bot = bots[1]
            ),
            Connections(
                user = users[0],
                bot = bots[1]
            ),
            Connections(
                user = users[2],
                bot = bots[0]
            )
        ]

        db.session.add_all(connections)
        db.session.commit()

        # NB: inside the app, messages sent by bots are distributed to ALL their followers
        #this functionality does not exist when seeding the database with dummy data 
        messages =[
            Messages(
                connection = connections[0],
                content = 'hey, check this out:',
                timestamp = datetime.now()
            ),
            Messages(
                connection = connections[2],
                content = 'how good is this',
                timestamp = datetime.now()
            )
        ]
        
        db.session.add_all(messages)
        db.session.commit()

        print('Table seeded')

    @app.route('/')
    def index():
        return 'Hello World!'

    return app
