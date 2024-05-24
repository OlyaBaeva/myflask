from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError

from app.models import User


class MyForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Username must have only letters, number, dots and underscore')])
    email = EmailField("Email: ", validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField("Phone: ", validators=[DataRequired()])
    since = StringField("From: ", validators=[DataRequired()])
    forend = StringField("To: ", validators=[DataRequired()])
    NameApart = StringField("Apartments: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("The email has already been registered")
class ReviewForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")