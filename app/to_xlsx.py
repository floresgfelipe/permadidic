import os
from app import app
from app.models import Alumno
from flask import url_for

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

    rt_dict['Teléfono'] = str(alumno.telefono)

    rt_dict['Correo'] = str(alumno.correo)

    rt_dict['Grado'] = alumno.get_grado()

    rt_dict['Grupo'] = str(alumno.grupo)

    if alumno.foto != 'none':
        rt_dict['Foto'] = ('https://catequesisver.org/fotos_admin/' 
                            + os.path.basename(alumno.foto))
    else:
        rt_dict['Foto'] = 'NO DISPONIBLE'

    if alumno.boleta_carta != 'none':
        rt_dict['Boleta'] = ('https://catequesisver.org/boletas_admin/' 
                                + os.path.basename(alumno.boleta_carta))
    else:
        rt_dict['Boleta'] = 'NO DISPONIBLE'

    return rt_dict


def alumnos_to_excel():
    alumnos = Alumno.query.all()
    lista_al = [alumno_to_dict(alumno) for alumno in alumnos]
    df = pd.DataFrame(lista_al)
    
    alumnos_1o = Alumno.query.filter_by(grado=1).all()
    lista_1o = [alumno_to_dict(alumno) for alumno in alumnos_1o]
    df1 = pd.DataFrame(lista_1o)

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
    df1.to_excel(writer, sheet_name='Primero', index=False)
    df2.to_excel(writer, sheet_name='Segundo', index=False)
    df3.to_excel(writer, sheet_name='Tercero', index=False)
    df4.to_excel(writer, sheet_name='Curso Esp.', index=False)

    writer.save()


def main():
    alumnos_to_excel()

if __name__ == '__main__':
    main()