from app import app
from flask import render_template
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/entrar')
def entrar():
    form = LoginForm()
    return render_template('entrar.html', title='Entrar al Curso', form=form)
