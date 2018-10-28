from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>', methods=('GET', 'POST'))
def index(user_id):
    db = get_db()
    info = db.execute(
        'SELECT * FROM user WHERE id = ?',
        (user_id,)
    )
    reputation = db.execute(
        'SELECT * FROM history where id = ?',
        (user_id,)
    )
    return render_template('profile/index.html', info=list(info.fetchone()))
