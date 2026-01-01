# main.py
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis
import stripe
from celery import Celery
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.utcnow() + timedelta(days=1)
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
stripe.api_key = os.environ.get('STRIPE_API_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
redis_store = FlaskRedis(app)
jwt = JWTManager(app)

celery = Celery(app.name, broker='amqp://localhost')
celery.conf.beat_schedule = {
    'send-notification': {
        'task': 'send_notification',
        'schedule': 60.0,  # run every minute
    },
}

from models import Produit, Utilisateur, Commande, Paiement, Notification
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
