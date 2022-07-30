from app import app, db
from app.models import Alumno, Admin, Evaluacion, Grado

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Alumno': Alumno, 
        'Admin': Admin, 
        'Evaluacion' : Evaluacion, 
        'Grado' : Grado    
    }
    