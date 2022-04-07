""" Forms for the Flask App """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from my_first_app.models import User


class SignupForm(FlaskForm):
    """
    A class to represent a sign up form.

    Attributes
    ----------
    first_name : str
        first name of the user
    last_name : str
        family name of the user
    email : str
        email of the user
    password: str
        password of the user
    repeat_password: str
        user needs to repeat the password from previous field

    Methods
    -------
    validate_email(self, email):
        Checks whether user is already registered or not.
    """
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(),
                                                EqualTo('password',
                                                        message='Passwords must match')])

    def validate_email(self, email):
        '''
            Returns an error if the email address already in use for another user.

                Parameters:
                    email (str): an email of the user

                Returns:
                    ValidationError: if the email already in use
        '''
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    """
        A class to represent a login form.

        Attributes
        ----------
        email : str
            email of the user
        password: str
            user's password
        remember: bool
            remember user for the session

        Methods
        -------
        validate_email(self, email):
            Checks whether user is already registered or not.

        validate_password(self, password):
            Checks whether password matches the one in the database.
        """
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        '''
            Returns an error if the email address is not registered.

                Parameters:
                    email (str): an email of the user

                Returns:
                    ValidationError: if the email is not registered
        '''
        person = User.query.filter_by(email=email.data).first()
        if person is None:
            raise ValidationError('An account is not registered for that email address')

    def validate_password(self, password):
        '''
            Returns an error if the password does not match the record.

                Parameters:
                    password (str): user's password

                Returns:
                    ValidationError: if the password is wrong
        '''
        person = User.query.filter_by(email=self.email.data).first()
        if person is not None:
            check = person.check_password(password.data)
            if check is False:
                raise ValidationError('Wrong password!')


class ContactForm(FlaskForm):
    """
        A class to represent a contact us form.

        Attributes
        ----------
        full_name : str
            full name of the user
        email : str
            email of the user
        message : str
            message of the user
        """
    full_name = StringField(label='Your full name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    message = StringField(label='Message')
    submit = SubmitField(label="Submit")
