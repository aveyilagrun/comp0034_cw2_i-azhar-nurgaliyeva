from datetime import datetime, timedelta
import requests
from flask import Blueprint, render_template, flash
from flask_login import current_user

index_bp = Blueprint('index_bp', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        flash(f'Hello {name}. ')

    api_key = '5d543664bed14ca1b6ae2a6d698c3d58'
    search = 'Transport for London'
    newest = datetime.today().strftime('%Y-%m-%d')
    oldest = (datetime.today() - timedelta(hours=1)).strftime('%Y-%m-%d')
    sort_by = 'publishedAt'
    url = f'https://newsapi.org/v2/everything?q={search}&from={oldest}&to={newest}&sortBy={sort_by}'

    response = requests.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(api_key)
    })

    news = response.json()

    return render_template('index.html', title='Home page', news=news)


@index_bp.route('/about')
def about_info():
    return render_template('about.html', title='About visualisations')


@index_bp.route('/references')
def references():
    return render_template('references.html', title='References')
