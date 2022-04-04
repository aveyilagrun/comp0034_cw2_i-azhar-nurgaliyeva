from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    return render_template('index.html', title="Home")
