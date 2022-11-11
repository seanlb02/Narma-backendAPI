import os
from Controllers.bots_controller import bots_bp
from Controllers.users_controller import users_bp
from Controllers.auth_controller import auth_bp
from Controllers.connections_controller import connections_bp
from Controllers.messages_controller import messages_bp
from Controllers.likes_controller import likes_bp
from Controllers.content_controller import content_bp
from Models.Bot import Bot
from Models.Users import User
from Models.Connections import Connections
from Models.Messages import Messages
from Models.Likes import Likes
from Models.Content import Content
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from db import db, ma, bcrypt, jwt, generate_password_hash
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
    app.register_blueprint(content_bp)

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
                picture='stock image',
                age = '37'
            ),
            Bot(
                name='Mary',
                bio='Hey, im mary. I love everything fitness!',
                gender='Female',
                picture='stock image',
                age = '29'
            )
        
        ]

        db.session.add_all(bots)
        db.session.commit()

        users = [
            User(
                name='Peter Parker',
                email='peter@hotmail.com',
                password='password',
                phonenumber='+61414346614',
                gender='Male',
                age='2000-10-6',

            ),
            User(
                name='Debbie harry',
                email='deb@hotmail.com',
                password='password1',
                phonenumber='+61420956947',
                gender='Non-binary',
                age='1994-06-03',
            ),
            User(
                #admin user
                name='Jeremih something',
                email='jerryj@gmail.com',
                password=bcrypt.generate_password_hash('password666').decode('utf-8'),
                phonenumber='+61404966779',
                gender='Other',
                age='1990-2-5',
                is_admin=True,
            ), 
            User(
                #admin user
                name='Sean Connery',
                email='seanc@gmail.com',
                password=bcrypt.generate_password_hash('password3').decode('utf-8'),
                phonenumber='+61420956947',
                gender='Other',
                age='1990-2-5',
                is_admin=True,
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
        
        content = [
            Content(
                bot = bots[0],
                content = "hey this is content: www.google.com"
            ),
            Content(
                bot = bots[0],
                content = "content 2 isnfiusd"
            ),
            Content(
                bot = bots[1],
                content = "hey this is content: www.google.com"
            ),
            Content(
                bot = bots[1],
                content = "content 2 isnfiusd"
            ),
            
            
        ]

        db.session.add_all(content)
        db.session.commit()

        # NB: inside the app, messages sent by bots are distributed to ALL their followers
        #this functionality does not exist when seeding the database with dummy data 
        messages =[
            Messages(
                connection = connections[3],
                content = content[0],
                timestamp = datetime.now()
            ),
            Messages(
                connection = connections[3],
                content = content[1],
                timestamp = datetime.now()
            ),
            Messages(
                connection = connections[0],
                content = content[3],
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
