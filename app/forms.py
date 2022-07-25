from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_wtf.recaptcha import RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)

class LoginForm(FlaskForm):
    username = StringField('Correo Electrónico', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    recaptcha = RecaptchaField()
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[
        DataRequired(), 
        Length(min=6, 
        max=100)
    ])

    parroquia = StringField('Parroquia', validators=[
        DataRequired(), 
        Length(min=6, 
        max=100)
    ])

    decanato = StringField('Decanato', validators=[
        DataRequired(),
        Length(min=6, 
        max=50)
    ])

    grado = SelectField('Grado al que se inscribe', choices=[
        ('primero', '1o'), 
        ('segundo', '2o'), 
        ('tercero', '3o'),
        ('cuarto', '4o')
    ])

    boleta = FileField('Boleta del curso PERMANENTE anterior', validators=[
        FileRequired(), 
        FileAllowed(images)
    ])

    telefono = StringField('Celular Personal', validators=[
        DataRequired(),
        Length(min=10, 
        max=10)
    ])

    correo = StringField('Correo electrónico', validators=[
        DataRequired(),
        Regexp('\A[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\Z')
    ])

    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(),
        EqualTo('confirmacion')
    ])

    confirmacion = PasswordField(
        'Escribe otra vez la contraseña', 
        validators=DataRequired()
    )

    foto = FileField('Foto (Selfie)', validators=[
        FileRequired(), 
        FileAllowed(images)
    ])

    recaptcha = RecaptchaField()

    submit = SubmitField('Enviar')
    