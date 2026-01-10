from flask import Flask, redirect
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("https://illusionoir.github.io/anvi", code=302)

def run_web() -> None:
    app.run(host="0.0.0.0", port=8080)

def start_web() -> None:
    Thread(target=run_web, daemon=True).start()

