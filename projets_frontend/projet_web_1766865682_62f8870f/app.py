from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_elasticsearch import Elasticsearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
app.config['ELASTICSEARCH_URL'] = 'http://localhost:9200'

db = SQLAlchemy(app)
redis_store = FlaskRedis(app)
es = Elasticsearch(app.config['ELASTICSEARCH_URL'])

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([r.to_dict() for r in resources])

@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    resource = Resource(name=data['name'], description=data['description'])
    db.session.add(resource)
    db.session.commit()
    redis_store.set('resource_id', resource.id)
    es.index(index='resources', doc_type='resource', body=resource.to_dict())
    return jsonify({'id': resource.id})

@app.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(resource.to_dict())

@app.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    data = request.get_json()
    resource.name = data['name']
    resource.description = data['description']
    db.session.commit()
    es.index(index='resources', doc_type='resource', body=resource.to_dict())
    return jsonify({'id': resource.id})

@app.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    db.session.delete(resource)
    db.session.commit()
    redis_store.delete('resource_id')
    return jsonify({'id': id})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
