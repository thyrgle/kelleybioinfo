from flask import (
    Blueprint,
    render_template,
)
from . import models
from sqlalchemy import func
from libgravatar import Gravatar


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>', methods=('GET', 'POST'))
def index(user_id):
    # TODO Is [0] the best option?
    # TODO Refactor redundancy!
    total_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id).first()[0]
    print(total_rep)
    alignment_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="Alignment").first()[0]
    print(alignment_rep)
    protein_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="Protein").first()[0]
    motifs_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="Motifs").first()[0]
    rna_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="RNA").first()[0]
    phylogeny_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="Phylogeny").first()[0]
    probability_rep = models.History.query.with_entities(
            func.sum(models.History.value)
        ).filter_by(user_id=user_id, category="Probability").first()[0]
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
