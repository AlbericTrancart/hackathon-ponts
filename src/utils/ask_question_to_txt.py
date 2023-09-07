from io import StringIO
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def open_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as text_file:
        return text_file.read()


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = text.split(
        ". "
    )  # Divisez le texte en phrases en utilisant un point suivi d'un espace comme séparateur.

    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "histoire.txt")
document = open_text_file(filename)
chunks = split_text(document)


def gpt3_completion(question):
    x = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "tu es un professeur"},
            {"role": "user", "content": question},
        ],
    )

    return x["choices"][0]["message"]["content"]


def ask_question_to_pdf(question):
    return gpt3_completion(
        question
        + document
        + " tu repondras a cette question en t'appuyant uniquement du document"
    )


def gpt3_question():
    x = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            #   {"role": "system", "content": "tu es un professeur"},
            #   {"role": "user", "content": "pose moi une question sur le document"},
            {
                "role": "system",
                "content": document + "pose moi une question sur le document",
            },
        ],
    )
    return x["choices"][0]["message"]["content"]


def gpt3_answer(reponse, la_question):
    x = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            #   {"role": "system", "content": "tu es un professeur"},
            #   {"role": "user", "content": "pose moi une question sur le document"},
            {
                "role": "system",
                "content": document
                + " : en te basant uniquement sur ce texte, est ce que "
                + reponse
                + " repond à la question : "
                + la_question
                + " ? Tu repondras par vrai si la reponse est bonne et faux si elle est fausse",
            },
        ],
    )
    return x["choices"][0]["message"]["content"]
