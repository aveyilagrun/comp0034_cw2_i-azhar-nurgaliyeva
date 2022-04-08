""" Coursework 2 - Flask App """

from flask_mail import Mail
from my_first_app import create_app
from my_first_app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)
mail = Mail(app)

if __name__ == '__main__':
    app.run()
