from flask import (
    Blueprint,
    render_template,
)
from . import models
from sqlalchemy import func
from libgravatar import Gravatar


bp = Blueprint('profile', __name__, url_prefix='/profile')


def get_category_points(user_id, category):
    result = models.History.query.with_entities(
        func.sum(models.History.value)
    ).filter_by(user_id=user_id, category=category).first()[0]
    if result is None:
        return 0
    else:
        return result


@bp.route('/<int:user_id>', methods=('GET', 'POST'))
def index(user_id):
    # TODO Is [0] the best option?
    # TODO Simplify further using kwargs?
    total_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id).first()[0]
    alignment_rep = get_category_points(user_id, "Alignment")
    protein_rep = get_category_points(user_id, "Protein")
    motifs_rep = get_category_points(user_id, "Motifs")
    rna_rep = get_category_points(user_id, "RNA")
    phylogeny_rep = get_category_points(user_id, "Phylogeny")
    probability_rep = get_category_points(user_id, "Probability")
    name = models.User.query.filter_by(user_id=user_id).first()
    img = Gravatar(name.email).get_image(default='identicon', size=200)
    return render_template('profile/index.html',
                           total_rep=total_rep,
                           alignment_rep=alignment_rep,
                           protein_rep=protein_rep,
                           motifs_rep=motifs_rep,
                           rna_rep=rna_rep,
                           phylogeny_rep=phylogeny_rep,
                           probability_rep=probability_rep,
                           name=name,
                           profile_image=img)
