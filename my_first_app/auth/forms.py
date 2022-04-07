from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email

from my_first_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        person = User.query.filter_by(email=email.data).first()
        if person is None:
            raise ValidationError('An account is not registered for that email address')

    def validate_password(self, password):
        person = User.query.filter_by(email=self.email.data).first()
        if person is not None:
            check = person.check_password(password.data)
            if check == False:
                raise ValidationError('Wrong password!')


class ContactForm(FlaskForm):
    full_name = StringField(label='Your full name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    message = StringField(label='Message')
    submit = SubmitField(label="Submit")
