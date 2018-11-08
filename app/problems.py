from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    session,
    request,
    url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from datetime import datetime
from . import models

bp = Blueprint('problems', __name__, url_prefix='/problems')


@bp.route('/alignment.html')
def alignment():
    return render_template('problems/alignment.html')


@bp.route('/protein.html')
def protein():
    return render_template('problems/protein.html')


@bp.route('/motifs.html')
def motifs():
    return render_template('problems/motifs.html')


@bp.route('/rna.html')
def rna():
    return render_template('problems/rna.html')


@bp.route('/phylogeny.html')
def phylogeny():
    return render_template('problems/phylogeny.html')


@bp.route('/probability.html')
def probability():
    return render_template('problems/probability.html')

@bp.route('test.html', methods=('GET',))
def test():
    user_id = session.get('user_id')
    cur_user = models.User.query.filter_by(id=user_id)
    # TODO use default values.
    models.db.session.add(models.History(
        id=user_id, 
        award=10))
    models.db.session.commit()
    return render_template('problems/test.html')
