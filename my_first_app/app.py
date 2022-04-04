from flask import Flask
from my_first_app import create_app
from my_first_app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)


# @app.route('/')
# def index():  # put application's code here
#     return 'This is the home page for my_first_app'


if __name__ == '__main__':
    app.run()
