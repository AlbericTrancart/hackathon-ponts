from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import ask_question_to_pdf


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
    document = ask_question_to_pdf.read_pdf(filename)
    doc = Text.query.get(0)
    if doc is not None:
        db.session.delete(doc)
        db.session.commit()
    db.session.add(Text(id=0, text=document))
    db.session.commit()
    return render_template('index.html', name=__name__)


@app.route('/prompt', methods=['POST'])
def handlePrompt():
    doc = db.get_or_404(Text, 0).text
    answer = ask_question_to_pdf.ask_question_to_pdf(request.form['prompt'],
                                                     doc)
    return {'answer': answer}


@app.route('/question', methods=['GET'])
def handleQuestionClick():
    doc = db.get_or_404(Text, 0).text
    question = ask_question_to_pdf.get_question_from_pdf(doc)
    return {'answer': question}


@app.route('/answer', methods=['POST'])
def handleAnswer():
    doc = db.get_or_404(Text, 0).text
    correction = ask_question_to_pdf.correct_with_pdf(
        request.form['prompt'], request.form['question'], doc)
    return {'answer': correction}


@app.route('/text', methods=['POST'])
def handleText():
    doc = db.get_or_404(Text, 0)
    doc.text = request.form['text']
    db.session.commit()
    titre = ask_question_to_pdf.get_title_from_pdf(doc.text)
    return {'answer': "Votre texte (" + titre + ") a bien été enregistré"}


@app.route('/pdf', methods=['POST'])
def uploadPdf():
    if "pdfUpload" in request.files:
        upfile = request.files['pdfUpload']
        upfilename = secure_filename(upfile.filename)
        upfile.save(os.path.join(app.config['UPLOAD_FOLDER'], upfilename))
        doc = db.get_or_404(Text, 0)
        upfilename = os.path.join(os.path.dirname(__file__),
                                  "uploads", upfilename)
        doc.text = ask_question_to_pdf.read_pdf(upfilename)
        db.session.commit()
        titre = ask_question_to_pdf.get_title_from_pdf(doc.text)
    return {'answer': "Votre texte (" + titre + ") a bien été enregistré"}
