from app import app
from flask import redirect, render_template, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from app.models import Alumno, Admin
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))

    form = LoginForm()
    if form.validate_on_submit():
        alumno = Alumno.query.filter_by(email=form.username.data).first()    
        if alumno is None or not alumno.check_password(form.password.data):
            flash('Correo o contraseña inválidos')
            return redirect(url_for('entrar'))
            
        login_user(alumno, remember=form.remember_me.data)
        session['account_type'] = 'Alumno'
        return redirect(url_for('perfil'))
    
    return render_template('entrar.html', title='Entrar al Curso', form=form)

@app.route('/login', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.username.data).first()    
        if admin is None or not admin.check_password(form.password.data):
            flash('Correo o contraseña inválidos')
            return redirect(url_for('login'))
            
        login_user(admin, remember=form.remember_me.data)
        session['account_type'] = 'Admin'
        return redirect(url_for('admin'))
    
    return render_template('entrar.html', title='Admin', form=form)

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('entrar'))

@app.route('/perfil')
def perfil():
    pass

@app.route('/admin')
def admin():
    pass