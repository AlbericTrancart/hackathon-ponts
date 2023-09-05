from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', name=__name__)


@app.route('/prompt', methods=['POST'])
def handlePrompt():
    prompt = request.form['prompt']
    return {'answer': prompt}
