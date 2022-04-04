from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        from my_first_app.models import User
        db.create_all()

    from my_first_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from my_first_app.main.routes import index_bp
    app.register_blueprint(index_bp)

    return app
