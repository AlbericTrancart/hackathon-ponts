import os
from flask import render_template
from flask import Flask
from flask import request, jsonify
from src.utils.ask_question_to_pdf import (
    gpt3_completion,
    validate_answer,
    add_information_historic,
    read_pdf,
    split_text,
)

app = Flask(__name__)


text = """pose moi une nouvelle question sur le
    texte sur le dernier cours que tu as appris !"""

new_text = """a partir de maintenant tu réactualise
    ton texte via les messages précedent"""

qcm = """pose moi un unique question à 3 choix de réponses
    sur le texte sur les ponts-et-chaussées sans donner la réponse"""

repA = """je choisis la reponse A a la question précedente, vérifie
en répondant d'abord par vrai ou faux puis la bonne reponse"""
repB = """je choisis la reponse B a la question précedente, vérifie
en répondant d'abord par vrai ou faux puis la bonne reponse"""
repC = """je choisis la reponse C a la question précedente, vérifie
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
    answer = gpt3_completion(input)
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def return_answer():
    input = request.form["prompt"]
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

@app.route("/cours", methods=["GET"])
def give_new_course():
    answer = gpt3_completion(
        """Demande à l'utilisateur d'envoyer le cours sur lequel il a des questions ou il veut que tu l'interroges. Quand il a envoyé le texte ne répond pas à son message mais attend qu'il te pose une question"""
    )
    return {"answer": answer}


@app.route("/upload", methods=["POST"])
def uploading(given_text=new_text):
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file.save("src/utils/filename.pdf")

    # filename = os.path.join(os.path.dirname(__file__), "src/utils/filename.pdf")
    # document = read_pdf(filename)
    # chunks = split_text(document)
    # print(chunks)
    for k in split_text(read_pdf("src/utils/filename.pdf")):
        add_information_historic(k)
        #print(k)

    # add_information_historic(chunks)
    return jsonify({"message": "File uploaded successfully"}), 200
