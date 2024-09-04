from flask import render_template
from flask import Flask
from flask import request
from src.utils.ask_question_to_pdf import gpt3_completion, validate_answer

app = Flask(__name__)


text = """pose moi une nouvelle question sur le
    texte sur les ponts-et-chaussées !"""


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

# used to check env files
