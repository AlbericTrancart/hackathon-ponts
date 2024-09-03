from flask import render_template
from flask import Flask
from flask import request
from ask_question_to_pdf import (
    gpt3_completion,
)

app = Flask(__name__)


text = "pose moi une nouvelle question sur le texte sur les ponts-et-chaussées !"


@app.route("/")
def hello_world():
    return """<p>Hello, World!<p> <a href="/hello"> click here <a>"""


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)


@app.route("/question", methods=["GET"])
def give_question(given_text=text):
    answer = gpt3_completion(given_text)
    return {"answer": answer}


@app.route("/prompt", methods=["POST"])
@app.route("/answer", methods=["POST"])
def return_prompt():
    input = request.form["prompt"]
    answer = gpt3_completion(input)
    return {"answer": answer}
