from flask import Flask
from flask import render_template
from flask import request

from src.utils.ask_question_to_pdf import ask_question_to_pdf, initialize_session

app = Flask(__name__)


@app.route("/")
def hello_world(name=None):
    return render_template("index.html", name=name)


@app.route("/prompt", methods=["POST"])
def prompt():
    question = request.form["prompt"]
    answer = ask_question_to_pdf(question)
    return {"answer": answer}


@app.route("/question", methods=["GET"])
def question():
    answer = ask_question_to_pdf("Pose-moi une question sur le texte.")
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def response():
    answer = request.form["prompt"]
    gpt_answer = ask_question_to_pdf(answer)
    return {"answer": gpt_answer}


@app.route("/file", methods=["POST"])
def upload_file():
    # Vérification si le fichier a bien été envoyé avec la requête
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]

    # Vérification si un fichier a été sélectionné
    if file.filename == "":
        return {"error": "No selected file"}, 400

    if file and file.filename.endswith(".pdf"):
        # Sauvegarde temporaire du fichier pour le lire
        file_path = "document.pdf"
        file.save(file_path)
        initialize_session()
        return {"response": file.filename}

    return {"error": "Invalid file type. Only PDFs are allowed."}, 400
