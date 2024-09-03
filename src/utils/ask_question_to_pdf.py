from io import StringIO
import os
import fitz
import openai
from openai import OpenAI
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()

def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()

client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")



def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
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


filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
document = read_pdf(filename)
chunks = split_text(document)


context = "Tu es un assistant qui me pose des questions pertinentes sur les cours que je t'envoie de sorte à être exhaustif sur les notions abordées."
def gpt3_completion():
    chunks_dic = []
    for t in chunks:
        chunks_dic.append({"role":"user", "content": t})
    msg = [{"role": "system", "content": context}]
    msg += chunks_dic
    msg += [
        {"role": "user", "content": "Pose moi une question assez précise sur ce texte et dis moi si la réponse est bien correcte en considérant les informations du texte."},
        {"role": "assistant", "content": "Quel était l'objectif initial de l'école ?"},
        {"role": "user", "content": " L'objectif initial de l'école était de former des ingénieurs capables de concevoir et de superviser la construction de routes et de ponts pour améliorer l'infrastructure en France."},
        {"role": "assistant", "content": "La réponse est correcte."},
        {"role": "user", "content": "Pose moi une nouvelle question sur le texte."}
    ]
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = msg
    )

    message = response.choices[0].message.content
    return message

