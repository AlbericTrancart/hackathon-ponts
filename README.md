# Hackathon Ponts ENPC

## Install

- when opening VSCode, install the suggested extensions (Python, Black Formatter and Pylance)
- create your python environment `python3 -m venv .venv`
- copy the `.env.example` file to a `.env` file
- replace the `OPENAI_API_KEY` and `OPENAI_ORGANIZATION` env variables with the real values
- activate your environment with `  `
- download necessary data with `python -m nltk.downloader all`
- run the server with `flask --app main run --debug`

The server should answer on http://localhost:5000

You can deactivate the environment with `deactivate`.

## Adding librairies

if you need to use a new librairies, you can do it with pip
`pip install [library name]` or `pip3 install [library name]`

## Project structure

Top-level layout:

- `main.py` — Flask application and routes
- `requirements.txt` — Python dependencies
- `templates/` — HTML templates (contains `index.html`)
- `static/` — static files (JS/CSS)
- `src/utils/` — utility modules used by the app
  - `ask_question_to_pdf.py` — functions to ask questions to PDF/text and interface with GPT
  - `ask_question_to_txt.py` — (alternate) text-based helper
  - `test_unitaire.py` — small unit test scaffolding
  - `histoire.txt`, `test.txt` — sample text files

## Endpoints

The Flask app exposes the following endpoints (see `main.py`):

- `GET /` - returns a small HTML/text ("Hello, World!")
- `GET /hello/` - renders the `index.html` template
- `POST /prompt` - expects a form field `prompt` and returns a JSON object `{ 'answer': ... }` from `ask_question_to_pdf`
- `GET /question` - returns a generated question via `gpt3_question()`
- `POST /answer` - expects a form field `prompt` and returns `{ 'answer': ... }` using `gpt3_answer`

Example curl (POST to `/prompt`):

```bash
curl -X POST -F "prompt=Quel est le résumé ?" http://127.0.0.1:5000/prompt
```

## Development notes

- The Flask app imports functions from `src/utils/ask_question_to_pdf.py`. If you change those utilities, restart the Flask server to pick changes.
- If you enable OpenAI features, make sure `OPENAI_API_KEY` is set and valid. The project currently expects the key to be available via environment variables.

## Adding dependencies

Install via pip and update `requirements.txt`:

```bash
pip install <package>
pip freeze > requirements.txt
```
