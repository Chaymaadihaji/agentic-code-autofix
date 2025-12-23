from flask import Flask, render_template
import random

app = Flask(__name__)

# Citations aléatoires
citations = [
    "La vie est belle.",
    "L'avenir est incertain.",
    "La liberté est précieuse.",
    "L'amitié est une valeur.",
    "La sagesse est une vertu.",
]

@app.route("/")
def index():
    # Sélection d'une citation aléatoire
    citation = random.choice(citations)
    return render_template("index.html", citation=citation)

if __name__ == "__main__":
    app.run(debug=True)
