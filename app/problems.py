from enum import Enum
from collections import namedtuple
import importlib
import functools
import os
from flask import (
    Blueprint,
    render_template,
    session,
)
from . import models


Entry = namedtuple('Entry', 'name url')


bp = Blueprint('problems',
               __name__,
               url_prefix='/problems',
               template_folder='templates/')


class Category(Enum):
    ALIGNMENT = 'alignment'
    PROTEIN = 'protein'
    RNA = 'rna'
    PROBABILITY = 'probability'
    MOTIFS = 'motifs'
    PHYLOGENY = 'phylogeny'

    def __str__(self):
        return str(self.value)


categories = {
    Category.ALIGNMENT: [],
    Category.PROTEIN: [],
    Category.RNA: [],
    Category.PROBABILITY: [],
    Category.MOTIFS: [],
    Category.PHYLOGENY: [],
}


render_problem = functools.partial(render_template, categories=categories)


@bp.route('/alignment.html')
def alignment():
    return render_problem('problems/default.html')


@bp.route('/protein.html')
def protein():
    return render_problem('problems/default.html')


@bp.route('/motifs.html')
def motifs():
    return render_problem('problems/default.html')


@bp.route('/rna.html')
def rna():
    return render_problem('problems/default.html')


@bp.route('/phylogeny.html')
def phylogeny():
    return render_problem('problems/default.html')


@bp.route('/probability.html')
def probability():
    return render_problem('problems/default.html')


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
    """
    Loads problems located in the "problem_collection" subdirectory.

    Note: A problem must have a NAME, URL, and CATEGORY value specified these
    values are then added to the categories global.
    """
    for f in os.listdir('./app/problem_collection'):
        # Takes (for exmaple) test.html becomes test
        no_ext = f.rsplit('.', 1)[0]
        spec = importlib.util.spec_from_file_location(no_ext,
                                                      'app/problem_collection/'
                                                      + f)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Add the module to categories.
        url = 'problems.' + module.URL.rsplit('.', 1)[0]
        categories[module.CATEGORY].append(Entry(name=module.NAME,
                                                 url=url))
        # Create a new rule for the the module and render with the modules' c-
        # ontent function.
        bp.add_url_rule(str(module.CATEGORY) + '/' + module.URL,
                        module.URL.rsplit('.', 1)[0],
                        module.content,
                        methods=('GET', 'POST'),
                        defaults={'level': 1})
