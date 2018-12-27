import random
from flask import request
from app import problems

NAME = "Needleman-Wunsch Algorithm"
CATEGORY = "RNA"
URL = "needlemanwunsch.html"


def validate(submission):
    pass


class NeedlemanWunsch:
    """
    Class used for generating Needleman-Wunsch matrices.
    """

    def _compute_block(self, result, i, j):
        """
        Given a block (corresponding to a 2 x 2 matrix), calculate the value o-
        f the bottom right corner.
        (Based on the equation:
                               M_{i,j} = max(M_{i-1,j-1} + S_{i,j},
                                             M_{i,j-1} + W,
                                             M_{i-1,j} + W)
         Found here: https://vlab.amrita.edu/?sub=3&brch=274&sim=1431&cnt=1)

        Args:
            result : The current matrix that is being computed.
            i : The right most part of the block being computed.
            j : The bottom most part of the block being computed.

        Returns:
            The value for the right bottom corner of a particular block.
        """
        return max(result[i-1][j-1] +
                   self._calc_weight(self._second_seq[i-1],
                                     self._first_seq[j-1]),
                   result[i-1][j] + self.gap,
                   result[i][j-1] + self.gap)

    def _calc_weight(self, first_char, second_char):
        """
        Helper function, given two characters determines (based on the sc-
        oring scheme) what the score for the particular characters can be.

        Args:
            first_char : A character to compare.
            second_char : A character to compare.

        Returns:
            Either self.match or self.mismatch.
        """
        if first_char == second_char:
            return self.match
        else:
            return self.mismatch

    def generate(self, first_seq, second_seq):
        """
        Generates a matrix corresponding to the scores to the Needleman-Wu-
        nsch algorithm.

        Args:
            first_seq : One of the sequences to be compared for similarity.
            second_seq : One of the sequences to be compared for
            similarity.

        Returns:
            A 2D list corresponding to the resulting matrix of the Needlem-
            an-Wunsch algorithm.
        """
        # Internally requies that the first sequence is longer.
        if len(second_seq) > len(first_seq):
            first_seq, second_seq = second_seq, first_seq
        self._first_seq = first_seq
        self._second_seq = second_seq
        # Adjust sequence with "intial space"
        # Initialize the resulting matrix with the initial row.
        result = [list(range(0, -len(first_seq) - 1, -1))]
        # Create initial columns.
        for i in range(-1, -len(second_seq) - 1, -1):
            row = [i]
            row.extend([0]*len(first_seq))
            result.append(row)
        # Sweep through and compute each new cell row-wise.
        for i in range(1, len(result)):
            for j in range(1, len(result[0])):
                result[i][j] = self._compute_block(result, i, j)
        # Format for prettier printing.
        for index, letter in enumerate(second_seq):
            result[index + 1].insert(0, letter)
        result[0].insert(0, ' ')
        result.insert(0, list("  " + first_seq))
        return result

    def __init__(self, match=1, mismatch=-1, gap=-1):
        """
        Initialize the Needleman-Wunsch class so that it provides weights for
        match (default 1), mismatch (default -1), and gap (default -1).
        """
        self.match = match
        self.mismatch = mismatch
        self.gap = gap
        self._first_seq = ""
        self._second_seq = ""


def deletion(seq, pos):
    """
    Deletes a random base pair from a sequence at a specified position.

    Args:
        seq : Sequence to perform deletion on.
        pos : Location of deletion.

    Returns:
        seq with character removed at pos.
    """
    return seq[:pos] + seq[pos:]


def base_change(seq, pos):
    """
    Changes a random base pair to another base pair at a specified position.

    Args:
        seq : Sequence to perform base change on.
        pos : Locaion of base change.

    Returns:
        seq with character changed at pos.
    """
    new_base = random.choice("ACTG".replace(seq[pos], ""))
    return seq[:pos] + new_base + seq[pos:]


def mutate(seq, rounds=3):
    """
    Mutates a piece of DNA by randomly applying a deletion or base change

    Args:
        seq : The sequence to be mutated.
        rounds : Defaults to 3, the number of mutations to be made.

    Returns:
        A mutated sequence.
    """
    mutations = (deletion, base_change)
    for _ in range(rounds):
        pos = random.randrange(len(seq))
        seq = random.choice(mutations)(seq, pos)
    return seq


def content():
    needleman_wunsch = NeedlemanWunsch()
    first_seq = ''.join(random.choices("ACTG", k=5))
    second_seq = mutate(first_seq)
    data = needleman_wunsch.generate(first_seq, second_seq)
    if request.method == 'POST':
        print("Form: {}".format(request.form))
        validate(request.form)
    # TODO: Automate first parameter!
    return problems.render_problem('problems/needlemanwunsch.html',
                                   matrix=data,
                                   sequences=[first_seq,
                                              second_seq])
