"""Models for the database"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from my_first_app import db


class User(db.Model, UserMixin):
    """ User class for the user table """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        """ Function to generate hashed password from the set one """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Function to check the hashed password """
        return check_password_hash(self.password, password)


class Messages(db.Model):
    """ Messages class for the messages table """
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.full_name} {self.email} {self.message}"
