""" Routes for the Flask App """

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, login_required
from datetime import timedelta
from flask_mail import Message

from my_first_app import db, login_manager
from my_first_app.auth.forms import SignupForm, LoginForm, ContactForm
from my_first_app.models import User, Messages

auth_bp = Blueprint('auth_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


def is_safe_url(target):
    """ Makes sure that target url is safe """
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    """ Makes sure that there is a safe redirect """
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/auth')
def index():
    """ Returns authentication section of the web app """
    return "This is the authentication section of the web app"


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Returns sign up section for the user """
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.first_name} {user.last_name}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth_bp.signup'))
        return redirect(url_for('index_bp.index'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Returns log in section of the web app """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user, remember=login_form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index_bp.index'))
    return render_template('login.html', title='Login', form=login_form)


@auth_bp.route('/logout')
@login_required
def logout():
    """ Log out function """
    logout_user()
    return redirect(url_for('index_bp.index'))


@auth_bp.route('/contact', methods=['GET', 'POST'])
def contact_us():
    """ Returns contact us section of the web app """
    from my_first_app.app import mail
    contact_form = ContactForm(request.form)
    if contact_form.validate_on_submit():
        user_request = Messages(full_name=contact_form.full_name.data,
                                email=contact_form.email.data,
                                message=contact_form.message.data)
        try:
            db.session.add(user_request)
            db.session.commit()
            flash(f"Thank you, {user_request.full_name}. Your message is received. "
                  f"Reference number: {user_request.id}")
            text = Message('Request is registered!',
                           sender='azharnurgaliyeva@yahoo.com',
                           recipients=[contact_form.email.data])
            text.body = f'''Thank you for your message! If you did not make this request then simply 
            ignore this email or contact us to remove this record. Here is the copy of it: 
            "{contact_form.message.data}". '''
            mail.send(text)
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register request for {contact_form.email.data}. ',
                  'error')
            return redirect(url_for('auth_bp.contact_us'))
        return redirect(url_for('index_bp.index'))
    return render_template('contact.html', title='Contact Us', form=contact_form)
