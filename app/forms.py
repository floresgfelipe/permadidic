from ast import Pass
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_wtf.recaptcha import RecaptchaField

class LoginForm(FlaskForm):
    username = StringField('Correo Electrónico', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired(), 
                            Length(min=6, max=100)])
    parroquia = StringField('Parroquia', validators=[DataRequired(), 
                            Length(min=6, max=100)])
    decanato = StringField('Decanato', validators=[DataRequired(),
                            Length(min=6, max=50)])
    telefono = StringField('Celular', validators=[DataRequired(),
                            Length(min=10, max=10)])
    correo = StringField('Correo electrónico', validators=[DataRequired(),
                            Regexp('\A[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\Z')])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(),
                                EqualTo('confirmacion')])
    confirmacion = PasswordField('Escribe otra vez la contraseña', 
                                 validators=DataRequired())
    recaptcha = RecaptchaField()
    