import os
from app import app, db
from app.models import Alumno

import pandas as pd


def alumno_to_dict(alumno):
    rt_dict = dict()

    rt_dict['Matrícula'] = str(alumno.matricula)

    rt_dict['Nombre'] = (str(alumno.nombres) 
                         + ' ' + str(alumno.apellido_p) 
                         + ' ' + str(alumno.apellido_m))
    

    rt_dict['Fecha de Nacimiento'] = (str(alumno.dia_nac) 
                                      + '/' + str(alumno.mes_nac) 
                                      + '/' + str(alumno.año_nac))

    rt_dict['Decanato'] = str(alumno.decanato)

    rt_dict['Parroquia'] = str(alumno.parroquia)

    rt_dict['Teléfono'] = int(alumno.telefono)

    rt_dict['Correo'] = str(alumno.correo)

    rt_dict['Grado'] = alumno.get_grado()

    rt_dict['Grupo'] = str(alumno.grupo)

    if alumno.foto != 'none':
        rt_dict['Foto'] = ('https://catequesisver.org/fotos_admin/' 
                            + os.path.basename(alumno.foto))
    else:
        rt_dict['Foto'] = 'NO DISPONIBLE'

    if alumno.boleta_carta != 'none':
        rt_dict['Boleta o Carta'] = ('https://catequesisver.org/boletas_admin/' 
                                + os.path.basename(alumno.boleta_carta))
    else:
        rt_dict['Boleta o Carta'] = 'NO DISPONIBLE'

    return rt_dict

def split_primero():
    alumnos_1o = Alumno.query.filter_by(grado=1).order_by(Alumno.id).all()
    c = 0

    for alumno in alumnos_1o:
        if c >= 98 and c <= 195:
            alumno.grupo = 'B'
            alumno.generar_matricula()
            db.session.commit()
        elif c > 195:
            alumno.grupo = 'C'
            alumno.generar_matricula()
            db.session.commit()

        c += 1


def alumnos_to_excel():
    alumnos = Alumno.query.all()
    lista_al = [alumno_to_dict(alumno) for alumno in alumnos]
    df = pd.DataFrame(lista_al)
    
    alumnos_1a = Alumno.query.filter_by(grado=1, grupo='A').all()
    lista_1a = [alumno_to_dict(alumno) for alumno in alumnos_1a]
    df1a = pd.DataFrame(lista_1a)

    alumnos_1b = Alumno.query.filter_by(grado=1, grupo='B').all()
    lista_1b = [alumno_to_dict(alumno) for alumno in alumnos_1b]
    df1b = pd.DataFrame(lista_1b)

    alumnos_1c = Alumno.query.filter_by(grado=1, grupo='C').all()
    lista_1c = [alumno_to_dict(alumno) for alumno in alumnos_1c]
    df1c = pd.DataFrame(lista_1c)

    alumnos_2o = Alumno.query.filter_by(grado=2).all()
    lista_2o = [alumno_to_dict(alumno) for alumno in alumnos_2o]
    df2 = pd.DataFrame(lista_2o)

    alumnos_3o = Alumno.query.filter_by(grado=3).all()
    lista_3o = [alumno_to_dict(alumno) for alumno in alumnos_3o]
    df3 = pd.DataFrame(lista_3o)

    alumnos_4o = Alumno.query.filter_by(grado=4).all()
    lista_4o = [alumno_to_dict(alumno) for alumno in alumnos_4o]
    df4 = pd.DataFrame(lista_4o)
    
    filename = os.path.join(app.config['EXCEL_PATH'], 'lista.xlsx')
    writer = pd.ExcelWriter(filename)

    df.to_excel(writer, sheet_name='General', index=False)
    df1a.to_excel(writer, sheet_name='1A', index=False)
    df1b.to_excel(writer, sheet_name='1B', index=False)
    df1c.to_excel(writer, sheet_name='1C', index=False)
    df2.to_excel(writer, sheet_name='2o', index=False)
    df3.to_excel(writer, sheet_name='3o', index=False)
    df4.to_excel(writer, sheet_name='Curso Esp.', index=False)

    writer.save()

def cambiar_grupo(id, grupo):
    al = Alumno.query.filter_by(id=id).first()
    al.grupo = grupo
    al.generar_matricula()
    db.session.commit()

def delete_alumno(id):
    al = Alumno.query.filter_by(id=id).first()
    db.session.delete(al)
    db.session.commit()


def main():
    alumnos_to_excel()

if __name__ == '__main__':
    main()