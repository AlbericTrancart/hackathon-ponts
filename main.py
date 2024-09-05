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
    prompt = (
        prompt
        + "\n"
        + "Est-ce la bonne réponse ? Réponds par vrai ou faux. Si c'est Faux, donne la bonne réponse."
    )
    ans = ask_q.gpt3_completion(prompt)
    s = jsonify({"answer": ans})
    return s

@app.route("/perro", methods=["POST", "GET"])
def perro():
    ans = ask_q.gpt3_completion("Incarnes Jean Rodolphe Perronnet (https://fr.wikipedia.org/wiki/Jean-Rodolphe_Perronet), présentes toi très rapidement et propose ton aide")
    s = jsonify({"answer": ans})
    return s

@app.route("/perro2", methods=["POST", "GET"])
def perro2():
    ans = ask_q.gpt3_completion("Réponds rapidement et relance la conversation")
    s = jsonify({"answer": ans})
    return s

@app.route("/dormieux2", methods=["POST", "GET"])
def dormieux2():
    ans = ask_q.gpt3_completion("Réponds rapidement et relance la conversation ")
    s = jsonify({"answer": ans})
    return s

@app.route("/dormieux", methods=["POST", "GET"])
def dormieux():
    ans = ask_q.gpt3_completion("Incarnes Luc Dormieux (https://fr.wikipedia.org/wiki/Luc_Dormieux), présentes toi très rapidement et enchaîne en proposant un exercice de mecanique")
    s = jsonify({"answer": ans})
    return s
