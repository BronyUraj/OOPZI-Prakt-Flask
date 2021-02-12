from flask import render_template
from app import app, db, json
from flask import request


@app.route("/")
def index():
    return "Hello"
