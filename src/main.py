import os

from flask import Flask, jsonify, request
from datetime import date, timedelta
from db import db, ma, bcrypt, jwt


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

    @app.cli.command('drop')
    def drop_db():
        db.drop_all()
        print('Tables dropped')
     
    @app.cli.command('create')
    def create_db():
        db.create_all()
        print('Tables created')





    @app.route('/')
    def index():
        return 'Hello World!'

    return app
