# config.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_talisman import Talisman
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'default-jwt-secret-key'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    Talisman(app)

    db = SQLAlchemy(app)
    jwt = JWTManager(app)

    from routes import bp
    app.register_blueprint(bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
