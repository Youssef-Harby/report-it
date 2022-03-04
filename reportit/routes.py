from flask import render_template, request
from reportit import app


@app.route('/form')
def index():
    return render_template('form.html')
