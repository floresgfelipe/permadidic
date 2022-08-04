from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from flask import session


class Alumno(UserMixin, db.Model):
    __tablename__ = 'alumno'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10))
    nombres = db.Column(db.String(50))
    apellido_p = db.Column(db.String(50))
    apellido_m = db.Column(db.String(50))
    decanato = db.Column(db.String(50))
    parroquia = db.Column(db.String(80))
    telefono = db.Column(db.String(10))    
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    foto = db.Column(db.String(120))
    grado = db.Column(db.Integer)
    grupo = db.Column(db.String(1))
    pago = db.Column(db.Integer)
    boleta = db.Column(db.String(120))
    servicio = db.Column(db.String(2))
    alumno_calificaciones = db.relationship(
        'Evaluacion', 
        secondary='calificaciones',
        back_populates='alumnos'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generar_matricula(self):
        c = 0
        if self.id < 10:
            c = '00' + str(self.id)
        elif self.id < 100:
            c = '0' + str(self.id)
        else:
            c = self.id

        self.matricula = str(self.grado) + \
             str(self.grupo) + str(self.nombres[0]) + c
    
    def get_grado(self):
        if self.grado == 1:
            return 'Primero'
        elif self.grado == 2:
            return 'Segundo'
        elif self.grado == 3:
            return 'Tercero'
        else:
            return 'Cuarto'
    
    def __repr__(self) -> str:
        return f'<Alumno {self.id} {self.matricula} {self.nombres} \
            {self.apellido_p} {self.apellido_m}>'

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(30))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<Admin {self.email} rol: {self.rol}>'


class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    alumnos = db.relationship(
        'Alumno',
        secondary='calificaciones',
        back_populates='alumno_calificaciones'
    )
    
    def __repr__(self) -> str:
        return f'<{self.nombre} {self.descripcion}>'

class Calificaciones(db.Model):
    __tablename__ = 'calificaciones'

    id_alumno = db.Column(ForeignKey('alumno.id'), primary_key=True)
    id_evaluacion = db.Column(ForeignKey('evaluacion.id'), primary_key=True)
    valor = db.Column(db.Integer, nullable=False)

class TicketSoporte(db.Model):
    __tablename__ = 'ticket_soporte'

    id =  db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    decanato = db.Column(db.String(50))
    parroquia = db.Column(db.String(80))
    telefono = db.Column(db.String(10))    
    email = db.Column(db.String(50))
    asunto = db.Column(db.Integer)
    comentario = db.Column(db.String(500))

@login.user_loader
def load_user(id):
    if session.get('account_type') == 'Admin':
        return Admin.query.get(int(id))
    elif session.get('account_type') == 'Alumno':
        return Alumno.query.get(int(id))
    else:
        return None


