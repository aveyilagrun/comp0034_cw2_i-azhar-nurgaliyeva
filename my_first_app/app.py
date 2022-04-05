from flask import Flask
from my_first_app import create_app
from my_first_app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
