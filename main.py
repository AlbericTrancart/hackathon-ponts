from flask import Flask
from flask import render_template
from flask import request
import ask_question_to_pdf
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', name=__name__)


@app.route('/prompt', methods=['POST'])
def handlePrompt():
    answer = ask_question_to_pdf.ask_question_to_pdf(request.form['prompt'])
    return {'answer': answer}


@app.route('/question', methods=['GET'])
def handleQuestionClick():
    question = ask_question_to_pdf.get_question_from_pdf()
    return {'answer': question}


@app.route('/answer', methods=['POST'])
def handleAnswer():
    correction = ask_question_to_pdf.correct_with_pdf(
        request.form['prompt'], request.form['question'])
    return {'answer': correction}
