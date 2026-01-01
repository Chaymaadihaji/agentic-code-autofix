python
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taches.db"
db = SQLAlchemy(app)


# modèle pour une tâche
class Tache(db.Model):
    __tablename__ = "taches"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)


# création de la base de données
@app.before_first_request
def créer_base_de_données():
    db.create_all()


# route pour accéder à la page d'accueil
@app.route("/")
def index():
    try:
        taches = Tache.query.all()
        return render_template("index.html", taches=taches)
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


# route pour ajouter une tâche
@app.route("/ajouter", methods=["POST"])
def ajouter_tache():
    try:
        nom = request.json["nom"]
        tache = Tache(nom=nom)
        db.session.add(tache)
        db.session.commit()
        return jsonify({"message": "Tâche ajoutée avec succès"})
    except KeyError:
        return jsonify({"erreur": "Le corps de la requête doit contenir un champ 'nom'"}), 400
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


# route pour supprimer une tâche
@app.route("/supprimer/<int:id>", methods=["DELETE"])
def supprimer_tache(id: int):
    try:
        tache = Tache.query.get(id)
        if tache:
            db.session.delete(tache)
            db.session.commit()
            return jsonify({"message": "Tâche supprimée avec succès"})
        else:
            raise NotFound("Tâche non trouvée")
    except NotFound as e:
        return jsonify({"erreur": str(e)}), 404
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
