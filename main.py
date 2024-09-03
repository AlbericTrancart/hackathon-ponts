from flask import Flask
from flask import render_template
from flask import request
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)

response = client.chat.completions.create(
  model="gpt-4.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prompt", methods = ['POST'])
def prompt():
    if request.method == 'POST':
        msg = request.form['prompt'].swapcase()
        return {"answer":msg}