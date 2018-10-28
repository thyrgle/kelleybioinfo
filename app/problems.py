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
from app.db import get_db
from datetime import datetime

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
    db = get_db()
    user_id = session.get('user_id')
    db.execute(
        '''
        UPDATE user 
        SET points = points + 10
        WHERE id = ?''', (user_id,)
    )
    db.commit()
    db.execute('INSERT INTO history (id, award, time_stamp) VALUES (?, ?, ?)',
                (user_id, 10, datetime.today().strftime('%Y-%m-%d'))
              )
    db.commit()
    return render_template('problems/test.html')
