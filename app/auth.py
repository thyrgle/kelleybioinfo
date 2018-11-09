import functools
from flask import (
    Blueprint, 
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from . import models


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functool.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif models.User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            models.db.session.add(models.User(username=username,
                                  password=generate_password_hash(password))
                          )
            models.db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
