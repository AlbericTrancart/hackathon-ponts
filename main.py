from flask import render_template
from flask import Flask
from flask import request
from src.utils.ask_question_to_pdf import (
    gpt3_completion,
    validate_answer,
    add_information_historic,
)

app = Flask(__name__)


text = """pose moi une nouvelle question sur le
    texte sur le dernier cours que tu as appris !"""


@app.route("/")
def front_page(name=None):
    return render_template("front_page.html", name=name)


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)


@app.route("/question", methods=["GET"])
def give_question(given_text=text):
    answer = gpt3_completion(given_text)
    return {"answer": answer}


@app.route("/prompt", methods=["POST"])
def return_prompt():
    input = request.form["prompt"]
    answer = gpt3_completion(input)
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def return_answer():
    input = request.form["prompt"]
    answer = validate_answer(input)
    return {"answer": answer}


@app.route("/cours", methods=["GET"])
def give_new_course():
    answer = gpt3_completion(
        """Demande à l'utilisateur d'envoyer le cours sur lequel il a des questions ou il veut que tu l'interroges. Quand il a envoyé le texte ne répond pas à son message mais attend qu'il te pose une question"""
    )
    return {"answer": answer}
