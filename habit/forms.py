from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import (Email, DataRequired, EqualTo, 
                                Length, ValidationError)

from habit import db
from habit.user import User

class RegisterForm(FlaskForm):
    email = StringField(
        "E-mail", 
        validators=[DataRequired(), Email(), Length(max=256)]
        )
    password = PasswordField(
        "Password", 
        validators=[DataRequired()]
        )
    password_check = PasswordField(
        "Password again", 
        validators=[DataRequired(), EqualTo("password")]
        )
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email address already in use!"
                )


class LoginForm(FlaskForm):
    email = StringField(
        "E-mail", 
        validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        "Password", 
        validators=[DataRequired()]
        )
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                "Email or password incorrect!"
                )


class HabitForm(FlaskForm):
    name = StringField(
        "Habit name", 
        validators=[DataRequired(), Length(max=256)]
        )
    color = RadioField(
        "Color", 
        choices=[
            ("black","Black"),
            ("red","Red"),
            ("tangerine","Tangerine"),
            ("orange","Orange"),
            ("peach","Peach"),
            ("yellow","Yellow"),
            ("green","Green"),
            ("cyan","Cyan"),
            ("teal","Teal"),
            ("indigo","Indigo"),
            ("blue","Blue"),
            ]
        )
    submit = SubmitField("check")
