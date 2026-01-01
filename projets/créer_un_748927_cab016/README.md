from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(100), nullable=False)
    choice = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(100), nullable=False)
    choice = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/score', methods=['POST'])
def score():
    player = request.form['player']
    choice = request.form['choice']
    score = 0
    historique = Historique(player=player, choice=choice)
    db.session.add(historique)
    db.session.commit()
    return render_template('score.html', player=player, score=score)

@app.route('/historique')
def historique():
    historiques = Historique.query.all()
    return render_template('historique.html', historiques=historiques)

if __name__ == '__main__':
    app.run(debug=True)
