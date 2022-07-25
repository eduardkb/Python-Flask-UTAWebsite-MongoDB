from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    # validation messages are optional. there is a default
    email       = StringField("Email", validators=[DataRequired("E-mail cannot be empty"), Email(message="Incorrect e-mail format")])
    password    = PasswordField("Password", validators=[DataRequired(message="Password must not be empty"), Length(min=6, max=20)])
    remember_me  = BooleanField("Remember Me")
    submit = SubmitField("login")

class RegisterForm(FlaskForm):
    email               = StringField("Email", validators=[DataRequired(), Email()])
                            # validator validates size of password
    password            = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)])
                            # validator equalto = validates if equal to password
    password_confirm    = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    first_name          = StringField("First Name", validators=[DataRequired(), Length(min=3, max=55)])
    last_name           = StringField("Last Name", validators=[DataRequired(), Length(min=3, max=55)])
    submit              = SubmitField("Register Now")

    # validate function below called automatically 
    # only if "_email" corresponds to a field (case sensitive)
    def validate_email(self, email):
        # searches for a user where e-mail matches
        # comparing email on DB and on passed field
        user = User.objects(email=email.data).first()
        # if there is a object, raise error that user already exists
        if user:
            raise ValidationError("Email is already in use. Pick another one.")