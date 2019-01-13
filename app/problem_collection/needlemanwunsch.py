import random
import operator
import functools
from collections import defaultdict
from flask import request
from app import problems

NAME = "Needleman-Wunsch Algorithm"
CATEGORY = "alignment"
URL = "needlemanwunsch.html"


class Cell:
    def __init__(self,
                 bottom_left=None,
                 top_left=None,
                 top_right=None,
                 main_entry=None):
        self.bottom_left = bottom_left
        self.top_left = top_left
        self.top_right = top_right
        self.main_entry = main_entry


def parse_submission(submission):
    """
    Parses the given submission data and reconstructs the original problem ma-
    trix and etracts the submission data.

    Args:
        submission : The data being submitted. It is a list of tuples. Each t-
        uple is either:
        ('hidden-x-y', Int) -> A cell in the matrix corresponding to a select-
        able position.
        ('csrf_token', tok) -> CSRF Token used for security purposes.
        ('submit', 'solution') -> Submission button (not needed, ignore).
        ('x-y', value) -> Cell selected by the user.

    Returns:
        A tuple of a reconstructed matrix for the first entry and a list of a-
        nswers for the second element.
    """
    # Bottom right corner matrix.
    main_matrix = defaultdict(lambda: defaultdict(Cell))
    answers = []

    # Collection of dispatch functions based on the kind of token being proce-
    # ssed.
    def add_to_matrix(row, col, data, corner='main_entry'):
        """ Add to the main entry corner of a cell in main_matrix"""
        nonlocal main_matrix
        setattr(main_matrix[row][col], corner, int(data))

    # Modify the main_entry slightly to incorprate the other corners.
    add_top_left = functools.partial(add_to_matrix, corner='top_left')
    add_top_right = functools.partial(add_to_matrix, corner='top_right')
    add_bottom_left = functools.partial(add_to_matrix, corner='bottom_left')

    def answer_submission(row, col, data):
        """
        Answer token was encounted, determine if it was chosen and add it
        to the answers data.
        """
        nonlocal answers
        if data == 'selected':
            answers.append((int(row), int(col)))

    def no_op(row, col, data):
        """ Handle submit and csrf tokens i.e. don't do anything. """
        return None

    tok_type_dispatch = {
        'csrf_token': no_op,
        'submit': no_op,
        'hidden': add_to_matrix,
        'topleft': add_top_left,
        'topright': add_top_right,
        'bottomleft': add_bottom_left,
        'answer': answer_submission
    }

    for token in submission.items():
        tok_type = token[0].rsplit('-')
        try:
            tok_type_dispatch[tok_type[0]](tok_type[1], tok_type[2], token[1])
        except IndexError:
            pass

    main_matrix = {row: sorted(list(cols.items()))
                   for row, cols in main_matrix.items()}
    main_matrix = sorted(list(main_matrix.items()))
    main_matrix = [entry[1] for entry in main_matrix]
    main_matrix = [list(map(lambda x: x[1], row)) for row in main_matrix]
    for ans in answers:
        main_matrix[ans[0]][ans[1]] = (main_matrix[ans[0]][ans[1]],
                                       'selected')
    return main_matrix


def traceback(problem_data, index=(-1, -1)):
    """
    Checks if the submission data is actually a valid path. Traces back throu-
    gh the grid to determine this.

    Args:
        problem_data : The grid for the problem.

    Returns:
        Boolean indicating whether the path is valid or not.
    """

    def index_to_corner(corner):
        if corner == 0:
            return (0, -1)
        if corner == 1:
            return (-1, -1)
        if corner == 2:
            return (-1, 0)

    # Check to see if we have finished the traceback.
    try:
        problem_data[index[0]][index[1]]
    except IndexError:
        return True
    # This cell wasn't selected, but it should have been.
    if not isinstance(problem_data[index[0]][index[1]], tuple):
        return False
    cell = problem_data[index[0]][index[1]][0]
    # Get the next best cell(s)
    best_value = cell.bottom_left
    best_corners = [0]
    corners = (cell.top_left, cell.top_right)
    for i, corner in enumerate(corners):
        if corner is None:
            # Check if last col or last row.
            try:
                problem_data[index[0]][index[1] - 1]
                best_corners = [0]
            except IndexError:
                best_corners = [2]
            continue
        if corner > best_value:
            best_corners = [i + 1]
            best_value = corner
        if corner == best_value:
            best_corners.append(i + 1)

    new_corners = list(map(lambda x: index_to_corner(x), best_corners))
    corner_results = list(map(lambda x: traceback(problem_data,
                                                  index=(index[0] + x[0],
                                                         index[1] + x[1])),
                              new_corners))
    result = functools.reduce(operator.or_, corner_results, False)
    return result


def validate(data):
    """
    Validates a correct solution to the Needleman-Wunsch algorithm.

    Args:
        data : A collection of "submission tokens".

    Returns:
        A boolean, True if the problem was correctly solved, False otherwise.
    """

    # Collect problem and answer data, merge into a matrix of the form:
    # [[Integer | Tuple (Integer | 'selected') ]]
    # TODO : ERROR IS HERE WITH PARSING OF DATA!
    problem_data = parse_submission(data)
    # TODO Find a better way to do this.
    # Check to make sure the first part of the problem was correctly selected.
    return traceback(problem_data)


class NeedlemanWunsch:
    """
    Class used for generating Needleman-Wunsch matrices.
    """

    def _compute_block(self,
                       top_left, top_right, bottom_left,
                       i, j):
        """
        Given a block (corresponding to a 2 x 2 matrix), calculate the value o-
        f the bottom right corner.
        (Based on the equation:
                               M_{i,j} = max(M_{i-1,j-1} + S_{i,j},
                                             M_{i,j-1} + W,
                                             M_{i-1,j} + W)
        Found here: https://vlab.amrita.edu/?sub=3&brch=274&sim=1431&cnt=1)
        All components of the arguments of the max function are also returned.

        Args:
            top_left : The cell touching the left corner of the current cell.
            top_right : The cell directly above the left corner of the current
            cell.
            bottom_left : The cell directly to the left of the current cell.
            i : The current row of the cell being computed.
            j : The current column of the cell being computed.

        Returns:
            The values for the right bottom corner of a particular block.
        """
        top_left_corner = top_left + \
            self._calc_weight(self._second_seq[i-1],
                              self._first_seq[j-1])
        top_right_corner = top_right + self.gap
        bottom_left_corner = bottom_left + self.gap
        bottom_right_corner = max(top_left_corner,
                                  bottom_left_corner,
                                  top_right_corner)
        return Cell(top_left=top_left_corner,
                    top_right=top_right_corner,
                    bottom_left=bottom_left_corner,
                    main_entry=bottom_right_corner)

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
        result[0] = [Cell(None, None, None, entry) for entry in result[0]]
        # Create initial columns.
        for i in range(-1, -len(second_seq) - 1, -1):
            row = [Cell(None, None, None, i)]
            # TODO : Check for possible reference confusion.
            row.extend([Cell(None, None, None, 0)]*len(first_seq))
            result.append(row)
        # Sweep through and compute each new cell row-wise.
        for i in range(1, len(result)):
            for j in range(1, len(result[0])):
                top_left = result[i-1][j-1].main_entry
                top_right = result[i-1][j].main_entry
                bottom_left = result[i][j-1].main_entry
                result[i][j] = self._compute_block(top_left,
                                                   top_right,
                                                   bottom_left,
                                                   i,
                                                   j)
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
        print(validate(request.form))
    if len(first_seq) < len(second_seq):
        first_seq, second_seq = second_seq, first_seq
    return problems.render_problem('problems/needlemanwunsch.html',
                                   matrix=data,
                                   sequences=[first_seq,
                                              second_seq])
