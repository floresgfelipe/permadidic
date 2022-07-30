from datetime import datetime
from app import db

class Alumno(db.Model):
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

    def __repr__(self) -> str:
        return f'<Alumno {self.matricula} {self.nombres} \
            {self.apellido_p} {self.apellido_m}>'

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(30))

    def __repr__(self) -> str:
        return f'<Admin {self.email} rol: {self.rol}>'

class Grado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    año = db.Column(db.String(4))   

    def __repr__(self) -> str:
        return f'<Grado {self.nombre} generación: {self.año}>'

class Inscripcion(db.Model):
    id_grado = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, primary_key=True)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, index=True)
    fecha_validacion = db.Column(
        db.DateTime, 
        index=True, 
        default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f'<Pago validado en {self.fecha_validacion}>'

class Boleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, index=True)
    filepath = db.Column(db.String(50))

class Evaluacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f'<{self.nombre} {self.descripcion}>'

class Calificacion(db.Model):
    id_evaluacion = db.Column(db.Integer, primary_key=True)
    id_grado = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String(30))

    def __repr__(self) -> str:
        return f'<{self.id_alumno} {self.valor}>'
