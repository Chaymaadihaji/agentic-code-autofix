# main.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
app.config['ES_HOST'] = 'localhost'
app.config['ES_PORT'] = 9200

db = SQLAlchemy(app)
redis_store = FlaskRedis(app)
es = Elasticsearch(hosts=[app.config['ES_HOST']], port=app.config['ES_PORT'])

# Modèle de données
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if request.method == 'POST':
        resource_name = request.form['resource_name']
        resource_description = request.form['resource_description']
        resource = Resource(name=resource_name, description=resource_description)
        db.session.add(resource)
        db.session.commit()
        redis_store.set(f'resource:{resource_name}', resource.id)
        es.index(index='resources', body={'name': resource_name, 'description': resource_description})
        return jsonify({'message': 'Réservation créée avec succès'})
    resources = Resource.query.all()
    return render_template('reservations.html', resources=resources)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    results = es.search(index='resources', body={'query': {'match': {'name': query}}})
    return jsonify(results['hits']['hits'])

# Erreurs
@app.errorhandler(404)
def not_found(e):
    return jsonify({'message': 'Ressource non trouvée'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Erreur interne du serveur'}), 500

if __name__ == "__main__":
    app.run(debug=True)
