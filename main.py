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
    texte sur les ponts-et-chaussées !"""

qcm = """pose moi un unique question à 3 choix de réponses
    sur le texte sur les ponts-et-chaussées sans donner la réponse"""

repA = """je choisis la reponse A a la question précedente, vérifie
en répondant d'abord par vrai ou faux puis la bonne reponse"""
repB = """je choisis la reponse A a la question précedente, vérifie
en répondant d'abord par vrai ou faux puis la bonne reponse"""
repC = """je choisis la reponse A a la question précedente, vérifie
en répondant d'abord par vrai ou faux puis la bonne reponse"""


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
    add_information_historic(
        """Vérifie que le prochain message est en rapport avec le texte du
        l'Ecole des Ponts"""
    )
    answer = gpt3_completion(input)
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def return_answer():
    input = request.form["prompt"]
    add_information_historic(
        """Vérifie que le prochain message est en rapport avec le texte du
        l'Ecole des Ponts"""
    )
    answer = validate_answer(input)
    return {"answer": answer}


@app.route("/qcm", methods=["GET"])
def give_qcm(given_text=qcm):
    answer = gpt3_completion(given_text)
    return {"answer": answer}


@app.route("/repA", methods=["GET"])
def reponseA(given_text=repA):
    answer = gpt3_completion(given_text)
    return {"answer": answer}


@app.route("/repB", methods=["GET"])
def reponseB(given_text=repB):
    answer = gpt3_completion(given_text)
    return {"answer": answer}


@app.route("/repC", methods=["GET"])
def reponseC(given_text=repC):
    answer = gpt3_completion(given_text)
    return {"answer": answer}
