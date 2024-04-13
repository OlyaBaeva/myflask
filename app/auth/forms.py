from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("log in")

class RegForm(FlaskForm):
    nick = StringField("Nickname: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), EqualTo('password2', message="Password doesn't match")])
    password2 = PasswordField("Confirm pasword: ", validators=[DataRequired()])
    submit = SubmitField("Register")


    def validate_nickname(self, field):
        if User.query.filter_by(nick=field.data).first():
            raise ValidationError("The nickname already exists")
