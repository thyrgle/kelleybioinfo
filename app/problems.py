from enum import Enum
from collections import namedtuple
import importlib
import functools
import os
from flask import (
    Blueprint,
    render_template,
    session,
    request,
)
from . import models


Entry = namedtuple('Entry', 'name url')


bp = Blueprint('problems',
               __name__,
               url_prefix='/problems',
               template_folder='templates/')


class Category(Enum):
    ALIGNMENT = 'Alignment'
    PROTEIN = 'Protein'
    RNA = 'RNA'
    PROBABILITY = 'Probability'
    MOTIFS = 'Motifs'
    PHYLOGENY = 'Phylogeny'

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
@bp.route('/protein.html')
@bp.route('/motifs.html')
@bp.route('/rna.html')
@bp.route('/phylogeny.html')
@bp.route('/probability.html')
def default():
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


def manage_content(content, validate, module_html):
    """
    Decorator for managing level loading for a route.

    Args:
        content : The content to be rendered.
        validate : The method for validating a problem.
        level : The level of the problem to be rendered.
        module_html : The name of the html template for the problem.
    Returns:
        A modified function that handles level changes automatically, so the p-
        roblem implementer does not need to worry about it.
    """
    def managed_route(level):
        if request.method == 'POST':
            result = validate(request.form)
            print(result)
            if result != "ERROR":
                if result is True:
                    user_id = session.get('user_id')
                    if user_id is not None:
                        # Refactor for multiple levels...
                        models.db.session.add(models.History(
                            user_id=user_id,
                            category="Alignment",
                            value=10))
                        models.db.session.commit()
                    return "success"
                else:
                    return "error"
            return content(level)
        return render_problem(module_html)
    return managed_route


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
        bp.add_url_rule(str(module.CATEGORY).lower() + '/' + module.URL,
                        module.URL.rsplit('.', 1)[0],
                        manage_content(module.content,
                                       module.validate,
                                       'problems/' + module.URL),
                        methods=('GET', 'POST'),
                        defaults={'level': 1})
