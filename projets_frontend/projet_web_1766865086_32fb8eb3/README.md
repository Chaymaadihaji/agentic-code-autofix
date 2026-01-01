from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jouer')
def jouer():
    return render_template('jouer.html')

@app.route('/niveaux')
def niveaux():
    return render_template('niveaux.html')

if __name__ == '__main__':
    app.run(debug=True)
