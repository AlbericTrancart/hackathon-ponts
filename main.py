from flask import render_template
from flask import Flask
from flask import request
from ask_question_to_pdf import (
    gpt3_completion,
    add_text_to_dialog,
    initialise_discut,
    input_question,
    add_text_to_discussion,
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return """<p>Hello, World!<p> <a href="/hello"> click here <a>"""


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    initialise_discut()
    return render_template("index.html", name=name)


@app.route("/question", methods=["GET"])
def give_question():
    input_question()
    answer = gpt3_completion()
    return {"answer": answer}


@app.route("/prompt", methods=["POST"])
def return_prompt():
    input = request.form["prompt"]
    add_text_to_discussion(input)
    answer = gpt3_completion()
    return {"answer": answer}
