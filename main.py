from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import ask_question_to_pdf
app = Flask(__name__)

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=False, nullable=False)


with app.app_context():
    db.create_all()

filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
document = ask_question_to_pdf.read_pdf(filename)


@app.route('/')
def hello_world():
    try:
        doc = db.get_or_404(Text, 0)
        if doc.text != document:
            doc.text = document
            db.session.commit()
    except:
        pass
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
        file = request.files['pdfUpload']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        doc = db.get_or_404(Text, 0)
        doc.text = ask_question_to_pdf.read_pdf(file.filename)
        db.session.commit()
        titre = ask_question_to_pdf.get_title_from_pdf(doc.text)
    return {'answer': "Votre texte (" + titre + ") a bien été enregistré"}
