from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world(name=None):
    return render_template('index.html', name=name)


@app.route("/prompt", methods=['POST'])
def prompt():
    return {"answer": request.form["prompt"]}
