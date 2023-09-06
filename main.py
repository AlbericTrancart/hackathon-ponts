from flask import Flask
from flask import render_template, request
from ask_question_to_pdf import ask_question_to_pdf, gpt3_question, gpt3_answer

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/hello/")
def hello():
    return render_template("index.html")


# Route pour la page d'accueil
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Accueil")


@app.route("/prompt", methods=["POST"])
def prompt():
    message = {}
    message["answer"] = ask_question_to_pdf(request.form["prompt"])
    return message


@app.route("/question", methods=["GET"])
def question():
    question_recue = gpt3_question()
    message = {}
    message["answer"] = question_recue
    return message


@app.route("/answer", methods=["POST"])
def answer():
    message = {}
    la_reponse = request.form["prompt"]
    # la_question = request.form["question"]
    message["answer"] = gpt3_answer(la_reponse)
    return message
