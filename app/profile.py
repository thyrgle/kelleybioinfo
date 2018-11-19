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
from sqlalchemy import func


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>', methods=('GET', 'POST'))
def index(user_id):
    # TODO Is [0] the best option?
    total_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id).first()[0]
    name = models.User.query.filter_by(user_id=user_id).first()
    history = models.History.query.filter_by(user_id=user_id)
    history = [item.as_javascript for item in history.all()]
    return render_template('profile/index.html',
                            total_rep=total_rep,
                            history=history,
                            name=name)
