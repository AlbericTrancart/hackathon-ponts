from flask import Flask
from flask import render_template
from flask import request

from src.utils.ask_question_to_pdf import ask_question_to_pdf

app = Flask(__name__)


@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)


@app.route("/prompt", methods=["POST"])
def prompt():
    question = request.form["prompt"]
    answer = ask_question_to_pdf(question)
    return {"answer": answer}


@app.route("/question", methods=["GET"])
def question():
    answer = ask_question_to_pdf("Pose-moi une question sur le texte.")
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form["prompt"]
    gpt_answer = ask_question_to_pdf(answer)
    return {"answer": gpt_answer}
