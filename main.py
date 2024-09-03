from flask import Flask
from flask import render_template
from flask import request, jsonify


###
import os
import openai
from openai import OpenAI
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")



def gt3_completion(question_user):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question_user}]
    )
    return response.choices[0].message.content

text = "Les voitures électriques offrent plusieurs avantages par rapport aux voitures à moteur thermique : 1. **Zéro émissions locales :** Les voitures électriques ne produisent pas d'émissions d'échappement locales, réduisant ainsi la pollution de l'air et les effets sur la santé. 2. **Moins de dépendance aux combustibles fossiles :** Les voitures électriques utilisent l'électricité, qui peut provenir de sources renouvelables comme le soleil et le vent, réduisant la dépendance aux combustibles fossiles.3. **Coûts de fonctionnement réduits :** Les voitures électriques ont moins de pièces mobiles et nécessitent moins d'entretien par rapport aux voitures à moteur thermique, ce qui peut réduire les coûts à long terme. 4. **Performance instantanée :** Les voitures électriques offrent un couple élevé dès le départ, ce qui signifie une accélération rapide et fluide sans la nécessité de changer de vitesses. 5. **Conduite silencieuse :** Les moteurs électriques sont beaucoup plus silencieux que les moteurs thermiques, offrant une expérience de conduite plus paisible. 6. **Amélioration de l'efficacité énergétique :** Les voitures électriques convertissent plus efficacement l'énergie électrique en mouvement par rapport aux moteurs à combustion interne. 7. **Réduction des émissions de gaz à effet de serre :** Même en tenant compte de l'émission de CO2 liée à la production d'électricité, les voitures électriques ont tendance à produire moins d'émissions de gaz à effet de serre sur leur cycle de vie par rapport aux voitures à essence. 8. **Innovation technologique :** Les voitures électriques stimulent le développement de nouvelles technologies, telles que les batteries plus performantes et les systèmes de recharge avancés. 9. **Réduction du bruit urbain :** La diminution du bruit des véhicules électriques contribue à réduire le niveau de bruit dans les zones urbaines. 10. **Subventions et incitations :** Dans de nombreux endroits, les voitures électriques bénéficient d'incitations gouvernementales, telles que des réductions fiscales ou des voies réservées. Il est important de noter que la transition vers les voitures électriques implique également des défis, tels que l'infrastructure de recharge en expansion, la gestion des matériaux des batteries et l'autonomie limitée par rapport aux voitures à essence sur de longs trajets. Cependant, les avantages en matière d'environnement et d'efficacité continuent de renforcer l'attrait des voitures électriques pour l'avenir de la mobilité."

def ask_question_to_pdf(question_user = 'Peux-tu me résumer ce texte ?'):
    return gt3_completion(question_user + text)
###



app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


#### version texte cours

# @app.route('/prompt', methods=['POST'])
# def answer():
#     error = None
#     ai_response = ask_question_to_pdf(request.form['prompt'])

#     return jsonify({"answer": ai_response})



# @app.route('/question', methods=['GET'])
# def handle_click_button():
#     error = None
#     ai_response = ask_question_to_pdf('Pose moi une question !')

#     return jsonify({"answer": ai_response})


# @app.route('/answer', methods=['POST'])
# def answer_click_button():
#     error = None
#     question = request.form['question']
#     rep = request.form['prompt']

#     ai_response = ask_question_to_pdf(f'Analyse ma réponse {rep} par rapport à ta question {question}. Ma réponse à ta question est - elle correcte?')

#     return jsonify({"answer": ai_response})


#### version PDF 



def read_pdf(filename):
    context = ""

    # Open the PDF file
    with open(filename) as pdf_file:
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



def ask_question_to_pdf_bis(question_user = 'Peux-tu me résumer ce texte ?'):
    text = read_pdf('filename.pdf')
    return gt3_completion(question_user + text)


@app.route('/prompt', methods=['POST'])
def answer():
    error = None
    ai_response = ask_question_to_pdf_bis(request.form['prompt'])

    return jsonify({"answer": ai_response})



@app.route('/question', methods=['GET'])
def handle_click_button():
    error = None
    ai_response = ask_question_to_pdf_bis('Pose moi une question !')

    return jsonify({"answer": ai_response})


@app.route('/answer', methods=['POST'])
def answer_click_button():
    error = None
    question = request.form['question']
    rep = request.form['prompt']

    ai_response = ask_question_to_pdf_bis(f'Analyse ma réponse {rep} par rapport à ta question {question}. Ma réponse à ta question est - elle correcte?')

    return jsonify({"answer": ai_response})


