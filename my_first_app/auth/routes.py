from flask import Blueprint, render_template, flash, redirect, url_for
from my_first_app.auth.forms import SignupForm

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/authentic')
def index():
    return "This is the authentication section of the web app"


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.first_name.data
        flash(f"Hello, {name}. You are signed up.")
        return redirect(url_for("index_bp.index"))
    return render_template('signup.html', title='Sign Up', form=form)
