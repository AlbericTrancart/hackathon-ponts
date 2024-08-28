import os
from flask import Flask, jsonify, render_template, request, session
from src.utils.ask_question_to_pdf import gpt3_completion


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")  # Replace with a secure key

@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)


@app.route("/prompt", methods=["POST"])
def send_message():
    if "conversation" not in session:
        session["conversation"] = []

    message = request.form["prompt"]
    session["conversation"].append({"role": "user", "content": message})

    return jsonify({"answer": gpt3_completion(session["conversation"])})
