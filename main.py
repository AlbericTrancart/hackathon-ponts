from flask import Flask
from flask import render_template
from flask import request


from src.utils.ask_question_to_pdf import ask_question_to_pdf

app = Flask(__name__)
path = "/Users/diaea/tp-hackathon/hackathon-ponts/filename.pdf"

@app.route("/")
def hello_world(name=None):
    return render_template('index.html', name=name)

@app.route("/prompt", methods=["GET",'POST'])
def response():
    res = request.form['prompt']
    answer = ask_question_to_pdf(res)
    #if not isinstance(answer, (str, dict, list)):
     #       answer = str(answer)
    return {"answer":answer}

a=''
@app.route("/question" , methods=['GET'])
def ask_question():
    qst = "poses moi une question concernant le texte"
    answer = ask_question_to_pdf(qst)
    return {"answer": answer}


@app.route("/answer" , methods=['POST'])
def ans_question():

    answ = request.form['prompt'] + " " + "Vérifie si ma réponse est juste, Sinon donnes moi la réponse correcte à cette question que tu viens de me poser" + " " + request.form['question']
    
    answer = ask_question_to_pdf(answ)
    
    return {"answer": answer}