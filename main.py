from flask import Flask, render_template, request, jsonify
import src.utils.ask_question_to_pdf

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/prompt', methods=['POST', 'GET'])
def prompt():
    if request.method == "POST":
        ans = src.utils.ask_question_to_pdf.gpt3_completion(request.form['prompt'])
        print(ans)
        s = jsonify({"answer": ans})
        return s
