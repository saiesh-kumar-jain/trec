from flask import Flask, redirect, url_for, render_template
from elasticsearch import Elasticsearch
import math

INDEX_NAME = 'maritime_accidents'
TYPE_NAME = 'document'
USERNAME = 'elastic'
PASSWORD = 'kVadsXwpJLKtIB7m4hlajnED'
es = Elasticsearch('https://35a530cd680844118e0642de8fc07b63.us-central1.gcp.cloud.es.io',
                   http_auth=(USERNAME, PASSWORD), scheme='https', port=9243, timeout=1000)

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    # //return "hello this is saiesh <h1>jain</h1>"
    return render_template("index.html", content = name, list =["Sai","jain","kumar"])

@app.route("/<name>")
def user(name):
    return  f"hello {name}"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = "jain"))

if __name__ == "__main__":
    app.run()
