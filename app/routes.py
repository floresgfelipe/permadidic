from app import app
from flask import redirect, render_template, url_for
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    form = LoginForm()
    
    if form.validate_on_submit():
        return redirect(url_for('entrar'))
    
    return render_template('entrar.html', title='Entrar al Curso', form=form)

@app.route('/curso-permanente', methods=['GET', 'POST'])
def curso_permanente():
    form = RegisterForm()

    if form.validate_on_submit():
        return redirect(url_for('perfil'))
    
    return render_template(
        'curso-permanente.html',
        title='Registro al Curso Permanente',
        form=form
    )

@app.route('/perfil')
def perfil():
    pass