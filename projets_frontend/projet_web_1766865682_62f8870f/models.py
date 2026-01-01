# models.py

import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/dbname'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
app.config['ELASTICSEARCH_URL'] = 'http://localhost:9200'

db = SQLAlchemy(app)
redis = FlaskRedis(app)
es = Elasticsearch(app.config['ELASTICSEARCH_URL'])

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    reservation = Reservation(start_date=data['start_date'], end_date=data['end_date'], resource_id=data['resource_id'], user_id=data['user_id'])
    db.session.add(reservation)
    db.session.commit()
    redis.incr('reservation_count')
    es.index(index='reservations', body={'start_date': data['start_date'], 'end_date': data['end_date'], 'resource_id': data['resource_id'], 'user_id': data['user_id']})
    return jsonify({'message': 'Reservation created'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = es.search(index='reservations', body={'query': {'match': {'start_date': query}}})
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
