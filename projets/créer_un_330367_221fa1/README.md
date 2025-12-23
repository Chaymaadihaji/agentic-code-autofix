from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taches.db"
db = SQLAlchemy(app)

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    statut = db.Column(db.String(50), nullable=False, default="En cours")

@app.route("/")
def index():
    taches = Tache.query.all()
    return render_template("index.html", taches=taches)

@app.route("/nouvelle_tache", methods=["POST"])
def nouvelle_tache():
    nom = request.form["nom"]
    description = request.form["description"]
    tache = Tache(nom=nom, description=description)
    db.session.add(tache)
    db.session.commit()
    return jsonify({"message": "Tâche créée avec succès"})

@app.route("/stats")
def stats():
    taches = Tache.query.all()
    stats = {}
    for tache in taches:
        statut = tache.statut
        if statut not in stats:
            stats[statut] = 1
        else:
            stats[statut] += 1
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
