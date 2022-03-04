from flask import render_template, request
from reportit import app
from reportit.form import *

@app.route('/')
def index():
    return render_template('form.html')