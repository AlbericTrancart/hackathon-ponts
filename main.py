from flask import Flask, render_template, request, jsonify
import src.utils.ask_question_to_pdf as ask_q

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    if request.method == "POST":
        req = request.form["prompt"]
        ans = ask_q.gpt3_completion(req)
        print(ans)
        s = jsonify({"answer": ans})
        return s
