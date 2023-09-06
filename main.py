from flask import Flask
from src.utils.ask_question_to_pdf import ask_question_to_pdf
from src.utils.ask_question_to_pdf import gpt3_question
from src.utils.ask_question_to_pdf import gpt3_answer

app = Flask(__name__)

la_question = "qui suis je ?"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

from flask import render_template

@app.route('/hello/')
def hello():
    return render_template('index.html')


from flask import request
@app.route('/prompt', methods=['POST'])
def prompt():
    message={}
    message ['answer'] = ask_question_to_pdf(request.form['prompt'])
    return message

@app.route('/question',methods=['GET'])
def question():
    la_question=gpt3_question()
    message={}
    message ['answer'] = la_question
    return message

@app.route('/answer',methods=['POST'])
def answer():
    message={}
    message['answer'] = gpt3_answer(request.form['prompt'],la_question)
    return message