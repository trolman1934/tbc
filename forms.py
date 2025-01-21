from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1)])
    description = StringField("description", validators=[DataRequired()])
    img = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), FileRequired()])
    submit = SubmitField('Save')


    submit = SubmitField('Save Product')
