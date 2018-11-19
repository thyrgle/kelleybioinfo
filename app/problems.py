from flask import (
    Blueprint,
    render_template,
    session,
)
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
    # TODO use default values.
    models.db.session.add(models.History(
        user_id=user_id,
        value=10))
    models.db.session.commit()
    return render_template('problems/test.html')
