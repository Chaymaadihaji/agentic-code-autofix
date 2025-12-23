from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap

app = Flask(__name__)
Bootstrap(app)

calculs = []
historique = []

@app.route("/")
def index():
    return render_template("index.html", calculs=calculs, historique=historique)

@app.route("/calcul", methods=["POST"])
def calcul():
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        op = request.form["op"]
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                raise ValueError
        calculs.append(f"{num1} {op} {num2} = {result}")
        historique.append({"calcul": f"{num1} {op} {num2} = {result}", "result": result})
        return jsonify({"result": result})
    except ValueError:
        return jsonify({"error": "Erreur de calcul"}), 400

@app.route("/historique")
def historique_route():
    return render_template("historique.html", historique=historique)

@app.route("/effacer_historique")
def effacer_historique():
    global historique
    historique = []
    return jsonify({"message": "Historique effacé"})

@app.route("/calculs")
def calculs_route():
    return jsonify(calculs)

if __name__ == "__main__":
    app.run(debug=True)
