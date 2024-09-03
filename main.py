from flask import Flask
from flask import render_template
from flask import request
from src.utils import ask_question_to_pdf

app = Flask(__name__)

#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/prompt', methods = ['POST'])
def bot_prompt():
    if request.method == 'POST':
        response = ask_question_to_pdf.gpt3_completion(request.form['prompt'])
        return {"answer":response}

