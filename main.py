from flask import render_template
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!<p>"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)


@app.route("/prompt", methods=["POST"])
def return_prompt():
    return {"answer": request.form["prompt"]}
