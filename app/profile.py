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
from . import models


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>', methods=('GET', 'POST'))
def index(user_id):
    info = models.User.query.filter_by(id=user_id)
    reputation = models.History.query.filter_by(id=user_id)
    return render_template('profile/index.html', info=info)
