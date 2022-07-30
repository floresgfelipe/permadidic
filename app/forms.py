from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    EqualTo,
)
from flask_wtf.recaptcha import RecaptchaField, Recaptcha


class LoginForm(FlaskForm):
    username = StringField(
    'Correo Electrónico', 
    validators=[DataRequired(message='Este campo es obligatorio')]
)

password = PasswordField(
    'Contraseña', 
    validators=[DataRequired(message='Este campo es obligatorio')]
)

remember_me = BooleanField('Recordarme')
recaptcha = RecaptchaField(validators=[
    Recaptcha(message='Error en la validación')
])

submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nombres = StringField('Nombre(s)', validators=[
        DataRequired(message='Este campo es obligatorio'), 
        Length(min=1, max=50, 
            message='El largo del nombre debe ser entre 1 y 50 caracteres')
    ])

    apellido_p = StringField('Apellido Paterno', validators=[
        DataRequired(message='Este campo es obligatorio'), 
        Length(min=1, max=50,
             message='El largo del apellido debe ser entre 1 y 50 caracteres')
    ])

    apellido_m = StringField('Apellido Materno', validators=[
        DataRequired(message='Este campo es obligatorio'), 
        Length(min=1, max=50,
             message='El largo del apellido debe ser entre 1 y 50 caracteres')
    ])

    decanato = SelectField(
        'Decanato',
        validators=[DataRequired(message='Este campo es obligatorio')],
        choices=[
            ('asuncion', 'Nuestra Señora de la Asunción'),
            ('cristo rey', 'Cristo Rey'),
            ('felipe', 'San Felipe de Jesús'),
            ('ana', 'Santa Ana'),
            ('jose', 'San José'),
            ('soledad', 'Soledad'),
            ('rosario', 'Nuestra Señora del Rosario'),
            ('guadalupe', 'Guadalupe'),
            ('inmaculada', 'Inmaculada')
        ], 
        render_kw={'autocomplete':'off'}
    )

    parroquia = SelectField(
        'Parroquia', 
        validators=[DataRequired(message='Este campo es obligatorio')], 
        choices=[
            
        ],
        render_kw={'autocomplete':'off'},
        validate_choice=False
    )

    grado = SelectField(
        'Grado al que se inscribe', 
        validators=[DataRequired(message='Este campo es obligatorio')], 
        choices=[
            (1, 'Primer Grado'), 
            (2, 'Segundo Grado'), 
            (3, 'Tercer Grado'),
            (4, 'Cuarto Grado')
        ],
        render_kw={'autocomplete':'off'}
    )

    telefono = StringField('Celular Personal', validators=[
        DataRequired(message='Este campo es obligatorio'),
        Length(min=10, max=10, 
            message='El númer celular debe ser de 10 dígitos')
    ])

    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message='Este campo es obligatorio'),
        Regexp('\A[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\Z',
            message='Dirección de correo inválida')
    ])

    contraseña = PasswordField(
        'Contraseña (min. 6 caracteres, max. 15 caracteres)', 
        validators=[
        DataRequired(message='Este campo es obligatorio'),
        EqualTo('confirmacion', 
            message='La contraseña y la confirmación deben coincidir'),
        Length(min=6, max=15,
            message='La contraseña debe tener entre 6 y 15 caracteres')
        ]
    )

    confirmacion = PasswordField(
        'Escriba otra vez la contraseña', 
        validators=[DataRequired(message='Este campo es obligatorio')]
    )

    recaptcha = RecaptchaField(validators=[
        Recaptcha(message='Error en la validación')
    ])

    submit = SubmitField('Enviar')

