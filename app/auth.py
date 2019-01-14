from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    session,
    url_for
)
from wtforms import (
    TextField,
    PasswordField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf import (
    FlaskForm,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from . import models


bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginForm(FlaskForm):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    email = EmailField('Email', [DataRequired()])


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from the da-
    tabase into ``g.user``."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = models.User.query.filter_by(user_id=user_id).first()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        error = None

        if not name:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif models.User.query.filter_by(username=name).first() is not None:
            error = 'User {} is already registered.'.format(name)

        if error is None:
            models.db.session.add(models.User(username=name,
                                  password=generate_password_hash(password),
                                  email=email))
            models.db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None
        user = models.User.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.user_id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
