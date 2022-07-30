from app import db

class Alumno(db.Model):
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
    id_grado = db.Column(db.Integer, db.ForeignKey('grado.id'))
    pago = db.Column(db.Integer)
    boleta = db.Column(db.String(120))
    calificaciones = db.relationship(
        'Evaluacion', 
        backref='calificacion', 
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        return f'<Alumno {self.matricula} {self.nombres} \
            {self.apellido_p} {self.apellido_m}>'

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(30))

    def __repr__(self) -> str:
        return f'<Admin {self.email} rol: {self.rol}>'

class Grado(db.Model):
    __tablename__ = 'grado'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    año = db.Column(db.String(4))  
    alumnos = db.relationship('Alumno', backref='grado', lazy='dynamic') 

    def __repr__(self) -> str:
        return f'<Grado {self.nombre} generación: {self.año}>'


class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id'))

    def __repr__(self) -> str:
        return f'<{self.nombre} {self.descripcion}>'
