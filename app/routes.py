from calendar import c
from app import app, db
from functools import wraps
from flask import (
    redirect, 
    render_template, 
    url_for, 
    flash, 
    session,
    request,
    redirect,
    url_for
)
from flask_login import current_user, login_user, logout_user
from app.models import Alumno, Admin
from app.forms import LoginForm, RegisterForm

def login_required_alumno(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('account_type') != 'Alumno':
            return redirect(url_for('entrar', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('account_type') != 'Admin':
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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
        alumno = Alumno.query.filter_by(
            apellido_p=form.apellido_p.data,
            apellido_m=form.apellido_m.data
        ).first()    
        if alumno is None:
            flash('No hay ningún alumno con esos apellidos')
            return redirect(url_for('entrar'))
        else:
            if (
                int(alumno.dia_nac) == int(form.dia_nac.data) and
                int(alumno.mes_nac) == int(form.mes_nac.data) and
                int(alumno.año_nac) == int(form.año_nac.data)
            ):  
                login_user(alumno, remember=form.remember_me.data)
                session['account_type'] = 'Alumno'
                return redirect(url_for('perfil'))
            else:
                flash('Fecha de nacimiento incorrecta')
                return redirect(url_for('entrar'))
    
    return render_template('entrar.html', title='Entrar al Curso', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))

    form = RegisterForm()

    if form.validate_on_submit():
        alumno = Alumno(
            matricula = 'none', 
            nombres = form.nombres.data,
            apellido_p = form.apellido_p.data,
            apellido_m = form.apellido_m.data,
            dia_nac = form.dia_nac.data,
            mes_nac = form.mes_nac.data,
            año_nac = form.año_nac.data,
            decanato = form.decanato.data,
            parroquia = form.parroquia.data,
            telefono = form.telefono.data,
            correo = form.correo.data,
            grado = form.grado.data,
            grupo = 'A',
            servicio = form.servicio.data
        )

        db.session.add(alumno)
        db.session.commit()

        alumno.generar_matricula()
        db.session.commit()

        login_user(alumno, remember=True)
        session['account_type'] = 'Alumno'
        return redirect(url_for('perfil'))  
    
    return render_template(
        'registro.html',
        title='Registro al Curso Permanente',
        form=form
    )

@app.route('/logout')
def logout():
    session.pop('account_type', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required_alumno
def perfil():
    return render_template('perfil.html', title='Perfil del Alumno')

@app.route('/admin')
@login_required_admin
def admin():
    pass

