import imghdr
import os
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
    url_for,
    abort,
    send_from_directory
)
from flask_login import current_user, login_user, logout_user
from app.models import Alumno, Admin, TicketSoporte
from app.forms import LoginForm, RegisterForm, UploadForm, ContactForm
from werkzeug.utils import secure_filename
from PIL import Image

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

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
        alumnos = Alumno.query.filter_by(
            apellido_p=form.apellido_p.data,
            apellido_m=form.apellido_m.data
        ).all()   
        if len(alumnos) == 0:
            flash('No hay ningún alumno con esos apellidos')
            return redirect(url_for('entrar'))
        else:
            for alumno in alumnos:
                if (
                    str(alumno.dia_nac) == str(form.dia_nac.data) and
                    str(alumno.mes_nac) == str(form.mes_nac.data) and
                    str(alumno.año_nac) == str(form.año_nac.data)
                ):  
                    login_user(alumno, remember=True)
                    session['account_type'] = 'Alumno'
                    return redirect(url_for('perfil'))

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
            nombres = form.nombres.data.strip(),
            apellido_p = form.apellido_p.data.strip(),
            apellido_m = form.apellido_m.data.strip(),
            dia_nac = form.dia_nac.data,
            mes_nac = form.mes_nac.data,
            año_nac = form.año_nac.data,
            decanato = form.decanato.data.strip(),
            parroquia = form.parroquia.data.strip(),
            telefono = form.telefono.data,
            correo = form.correo.data.strip(),
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
    return render_template(
        'perfil.html', 
        title='Perfil del Alumno', 
        basename=os.path.basename
    )

@app.route('/subir-foto', methods=['GET', 'POST'])
@login_required_alumno
def subir_foto():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.file.data
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                file_ext = str.lower(file_ext)
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                saved_filename = os.path.join(
                        app.config['UPLOAD_PATH_FOTOS'], 
                        current_user.get_id() + file_ext
                    )
                
                pic = Image.open(uploaded_file)
                pic.thumbnail((1200,1200))

                pic.save(saved_filename)
                
                current_user.foto = saved_filename
                db.session.commit()
            
            flash('La foto se ha subido exitosamente')
            return redirect(url_for('perfil'))
    return render_template('subir.html', title='Subir Foto', form=form)

@app.route('/fotos/<filename>')
@login_required_alumno
def fotos(filename):
    return send_from_directory(app.config['UPLOAD_PATH_FOTOS'], filename)

@app.route('/subir-boleta', methods=['GET', 'POST'])
@login_required_alumno
def subir_boleta():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.file.data
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                file_ext = str.lower(file_ext)
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                saved_filename = os.path.join(
                        app.config['UPLOAD_PATH_BOLETAS'], 
                        current_user.get_id() + file_ext
                    )

                uploaded_file.save(saved_filename)
                
                current_user.boleta_carta = saved_filename
                db.session.commit()

            flash('La boleta se ha subido exitosamente')
            return redirect(url_for('perfil'))
    return render_template('subir.html', title='Subir Foto', form=form)

@app.route('/boletas/<filename>')
@login_required_alumno
def boletas(filename):
    return send_from_directory(app.config['UPLOAD_PATH_BOLETAS'], filename)

@app.route('/admin')
@login_required_admin
def admin():
    pass

@app.route('/correccion-datos', methods=['GET', 'POST'])
@login_required_alumno
def correccion_datos():
    info = {
        'title' : 'Solicitud de Corrección de Datos',
        'label' : '¿Qué es lo que necesita ser corregido?'
    }
    
    form = ContactForm()

    if form.validate_on_submit():
        ticket = TicketSoporte(
            id_alumno = current_user.id,
            nombre = form.nombre.data,
            decanato = form.decanato.data,
            parroquia = form.parroquia.data,
            telefono = form.telefono.data,
            email = form.email.data,
            asunto = 0,
            comentario = form.comentario.data
        )

        db.session.add(ticket)
        db.session.commit()

        flash('Tu solicitud ha sido recibida')
        return redirect(url_for('perfil'))

    return render_template(
        'ayuda.html', 
        title='Corrección de Datos',
        form=form, 
        info=info
    )

@app.route('/ayuda', methods=['GET', 'POST'])
def ayuda():
    info = {
        'title' : 'Necesito ayuda para entrar',
        'label' : '¿En qué te podemos ayudar?'
    }
    
    form = ContactForm()

    if form.validate_on_submit():
        ticket = TicketSoporte(
            nombre = form.nombre.data,
            decanato = form.decanato.data,
            parroquia = form.parroquia.data,
            telefono = form.telefono.data,
            email = form.email.data,
            asunto = 1,
            comentario = form.comentario.data
        )

        db.session.add(ticket)
        db.session.commit()

        flash('Tu solicitud ha sido recibida')
        return redirect(url_for('entrar'))

    return render_template(
        'ayuda.html', 
        title='Ayuda para entrar',
        form=form, 
        info=info
    )
    