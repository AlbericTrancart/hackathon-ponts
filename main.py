from flask import Flask, render_template, request, jsonify
import src.utils.ask_question_to_pdf as ask_q

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ans = ask_q.gpt3_completion(prompt)
        s = jsonify({"answer": ans})
        return s


@app.route("/question", methods=["GET"])
def question():
    ans = ask_q.gpt3_completion("pose une question sur le texte")
    s = jsonify({"answer": ans})
    return s


@app.route("/answer", methods=["POST", "GET"])
def answer():
    prompt = request.form["prompt"]
    prompt = (prompt+
    +"Est-ce la bonne réponse ? Si ce n'est pas la bonne réponse, donne la bonne              réponse.")
    ans = ask_q.gpt3_completion(prompt)
    s = jsonify({"answer": ans})

    return s
