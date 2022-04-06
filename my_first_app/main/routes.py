from flask import Blueprint, render_template, flash
from flask_login import current_user

index_bp = Blueprint('index_bp', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        flash(f'Hello {name}. ')
    return render_template('index.html', title='Home page')

@index_bp.route('/about')
def about_info():
    return render_template('about.html', title='About visualisations')

@index_bp.route('/references')
def references():
    return render_template('references.html', title='References')


