import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taches.db"
db = SQLAlchemy(app)

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cree_le = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    modifie_le = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Statistique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_taches = db.Column(db.Integer, nullable=False)
    nombre_taches_terminees = db.Column(db.Integer, nullable=False)

@app.route("/")
def index():
    taches = Tache.query.all()
    statistiques = Statistique.query.first()
    if not statistiques:
        statistiques = Statistique(nombre_taches=0, nombre_taches_terminees=0)
        db.session.add(statistiques)
        db.session.commit()
    return render_template("index.html", taches=taches, statistiques=statistiques)

@app.route("/taches", methods=["POST"])
def ajouter_tache():
    titre = request.json["titre"]
    description = request.json["description"]
    tache = Tache(titre=titre, description=description)
    db.session.add(tache)
    db.session.commit()
    return jsonify({"message": "Tache ajoutée avec succès"})

@app.route("/taches/<int:id>", methods=["PUT"])
def modifier_tache(id):
    tache = Tache.query.get(id)
    if tache:
        titre = request.json.get("titre")
        description = request.json.get("description")
        if titre:
            tache.titre = titre
        if description:
            tache.description = description
        db.session.commit()
        return jsonify({"message": "Tache modifiée avec succès"})
    return jsonify({"message": "Tache non trouvée"}), 404

@app.route("/taches/<int:id>", methods=["DELETE"])
def supprimer_tache(id):
    tache = Tache.query.get(id)
    if tache:
        db.session.delete(tache)
        db.session.commit()
        return jsonify({"message": "Tache supprimée avec succès"})
    return jsonify({"message": "Tache non trouvée"}), 404

@app.route("/statistiques", methods=["GET"])
def get_statistiques():
    statistiques = Statistique.query.first()
    if statistiques:
        nombre_taches = Tache.query.count()
        nombre_taches_terminees = Tache.query.filter_by(modifie_le__isnull=False).count()
        statistiques.nombre_taches = nombre_taches
        statistiques.nombre_taches_terminees = nombre_taches_terminees
        db.session.commit()
    return jsonify({"nombre_taches": statistiques.nombre_taches, "nombre_taches_terminees": statistiques.nombre_taches_terminees})

if __name__ == "__main__":
    app.run(debug=True)
