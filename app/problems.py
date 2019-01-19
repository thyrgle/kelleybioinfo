from enum import Enum
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


# TODO : FIX THIS FUNCTION!
'''
def make_safe(func, url):
    """
    Decorator for determining whether the submit problem has not been user ta-
    mpered.

    Args:
        func :  Function used to check the correctness of a solution.
        url : The specific problem URL.

    Returns:
        A function that validates through the server, and then uses the valid-
        ation specified in func.
    """
    def validated_func():
        user_id = session.get('user_id')
        if user_id is not None:
            print("HERE")
            existing_problem = \
                models.Problem.query.filter_by(user=user_id,
                                               problem_type=url).first()
            if existing_problem:
                data = json.loads(existing_problem.data)
            else:
                data = func()
                models.add_problem(data, user_id, url)
        return data

    return validated_func
'''


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
        categories[module.CATEGORY].append(module.NAME)
        # Create a new rule for the the module and render with the modules' c-
        # ontent function.
        bp.add_url_rule(str(module.CATEGORY) + '/' + module.URL,
                        module.URL.rsplit('.', 1)[0],
                        module.content,
                        methods=('GET', 'POST'))
