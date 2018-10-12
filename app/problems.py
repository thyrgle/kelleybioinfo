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

bp = Blueprint('problems', __name__, url_prefix='/problems')


@bp.route('/alignment.html')
def alignment():
    return render_template('problems/alignment.html')
