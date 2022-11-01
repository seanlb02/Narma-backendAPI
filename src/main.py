import os

from flask import Flask, jsonify, request
from datetime import date, timedelta
from Controllers.bots_controller import bots_bp
from Controllers.users_controller import users_bp
from Controllers.auth_controller import auth_bp
from Controllers.connections_controller import connections_bp
from db import db, ma, bcrypt, jwt
from Models.Bot import Bot
from Models.Users import User
from Models.Connections import Connections


def create_app():
    app = Flask(__name__)

    #app-wide error handler
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404



    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app) 
    bcrypt.init_app(app)
    jwt.init_app(app)


        @app.route('/')
    def index():
        return 'Hello World!'

    return app