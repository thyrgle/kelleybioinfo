import importlib
import functools
import os
from flask import (
    Blueprint,
    render_template,
    session,
)
from . import models

bp = Blueprint('problems',
               __name__,
               url_prefix='/problems',
               template_folder='templates/')

categories = {
    'Alignment': [],
    'Protein': [],
    'RNA': [],
    'Probability': [],
    'Motifs': [],
    'Phylogeny': [],
}


render_problem = functools.partial(render_template, categories=categories)


@bp.route('/alignment.html')
def alignment():
    return render_template('problems/alignment.html',
                           categories=categories)


@bp.route('/protein.html')
def protein():
    return render_template('problems/protein.html',
                           categories=categories)


@bp.route('/motifs.html')
def motifs():
    return render_template('problems/motifs.html',
                           categories=categories)


@bp.route('/rna.html')
def rna():
    return render_template('problems/rna.html',
                           categories=categories)


@bp.route('/phylogeny.html')
def phylogeny():
    return render_template('problems/phylogeny.html',
                           categories=categories)


@bp.route('/probability.html')
def probability():
    return render_template('problems/probability.html',
                           categories=categories)


@bp.route('test.html', methods=('GET',))
def test():
    user_id = session.get('user_id')
    # TODO use default values.
    models.db.session.add(models.History(
        user_id=user_id,
        value=10))
    models.db.session.commit()
    return render_template('problems/test.html')


def load_problems():
    for f in os.listdir('./app/problem_collection'):
        no_ext = f.rsplit('.', 1)[0]
        spec = importlib.util.spec_from_file_location(no_ext,
                                                      'app/problem_collection/'
                                                      + f)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        categories[module.CATEGORY].append(module.NAME)
        print(module.CATEGORY + '/' + module.URL)
        bp.add_url_rule(module.CATEGORY + '/' + module.URL,
                        module.URL.rsplit('.', 1)[0],
                        module.content)
