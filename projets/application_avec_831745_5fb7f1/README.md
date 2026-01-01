# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class Formulaire(FlaskForm):
    nom_variable = StringField('Nom de variable', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Formulaire()
    if form.validate_on_submit():
        nom_variable = form.nom_variable.data
        # Gestion des caractères Unicode
        charactere_unicode = f"°{nom_variable}±"
        # Gestion des noms de variables avec accents
        nom_variable = nom_variable.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
        return redirect(url_for('resultat', nom_variable=nom_variable, charactere_unicode=charactere_unicode))
    return render_template('formulaire.html', form=form)

@app.route('/resultat', methods=['GET'])
def resultat():
    nom_variable = request.args.get('nom_variable')
    charactere_unicode = request.args.get('charactere_unicode')
    return render_template('resultat.html', nom_variable=nom_variable, charactere_unicode=charactere_unicode)

if __name__ == '__main__':
    app.run(debug=True)

# templates/formulaire.html

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulaire</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Formulaire</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.nom_variable.label }} {{ form.nom_variable() }}
            </div>
            <div class="form-group">
                {{ form.submit() }}
            </div>
        </form>
    </div>
</body>
</html>

# templates/resultat.html

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Résultat</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Résultat</h1>
        <p>Nom de variable : {{ nom_variable }}</p>
        <p>Caractère Unicode : {{ charactere_unicode }}</p>
    </div>
</body>
</html>
