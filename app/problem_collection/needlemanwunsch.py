import random
from collections import defaultdict
from flask import request
from app import problems

NAME = "Needleman-Wunsch Algorithm"
CATEGORY = "RNA"
URL = "needlemanwunsch.html"


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
    matrix = defaultdict(list)
    answer = []
    for token in submission.items():
        tok_type = token[0].rsplit('-')
        # ('hidden-x-y', Int) case
        if tok_type[0] == 'hidden':
            matrix[int(tok_type[1])].append(int(token[1]))
        # ('csrf_token', tok) and ('submit', 'solution') case
        elif tok_type[0] == 'csrf_token' or tok_type[0] == 'submit':
            pass
        # ('x-y', value) case
        else:
            answer.append((int(tok_type[0]), int(tok_type[1])))
    table = []
    for token in sorted(matrix.items()):
        try:
            table[token[0]].append(token[1])
        except IndexError:
            table.append(token[1])
    return table, answer


def next_best(data, cur_index):
    """
    Given a valid collection of problem data, find the next best route(s) down
    the problem matrix.
    *Note:* There may be multiple best next positions. This is why a list is
    always returned. There will be possibly more than one valid position.

    Args:
        data : A *valid* collection of problem data. (Note: This is a 2d list
        where each "row" consists of either a single number or a tuple. A tup-
        le indicates that the position was selected.)
        cur_index : The current position in the problem matrix. Represented as
        a tuple.

    Returns:
        A (list of) tuple(s) indicating where the next best choice(s) is in the
        matrix.
    """
    # Create a mapping for the "best" index. Consists of the index for:
    # Top right, and bottom left in that order.
    # (Omit top left, this will be placed in best and result by default.
    window = [(cur_index[0] - 1, cur_index[1]),
              (cur_index[0], cur_index[1] - 1)]
    # Assign best initially to the top right corner.
    best = (cur_index[0] - 1, cur_index[1] - 1)
    result = [best]
    # Determine the best corner(s).
    for corner in window:
        score = data[corner[0]][corner[1]]
        best_score = data[best[0]][best[1]]
        if isinstance(best_score, tuple):
            best_score = best_score[0]
        if isinstance(score, tuple):
            score = score[0]
        # TODO FIX THIS PLACE!
        if best_score == score:
            result.append(corner)
        elif best_score > score:
            result = []
            result.append(corner)
    return result


def indicies(x, data):
    """
    Given a list return *all* of the positions where a specified value is fou-
    nd.

    Args:
        x : The element to be found
        data : The data to search.

    Returns:
        A list of all location where x is found.
    """
    indicies = []
    cur_index = 0
    while True:
        try:
            cur_index = data.index(x, cur_index)
            indicies.append(cur_index)
            cur_index += 1
        except ValueError:
            return indicies
    # Should not be needed, but just in case...
    return indicies


def omit_invalid(index, data):
    """
    Helper function, attempts to return a value, if it isn't a valid entry, r-
    eturn nothing.

    Args:
        index : The attempted index.
        data : The data to access.

    Returns:
        Either the data or nothing.

    Notes:
        `index` is a tuple, and data is a 2D matrix (nested list).
    """
    try:
        check = data[index[0]][index[1]]
        return check
    except IndexError:
        return None


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
    problem_data, submission_data = parse_submission(data)
    # TODO Find a better way to do this.
    for answer in submission_data:
        row, col = answer[0], answer[1]
        problem_data[row][col] = (problem_data[row][col], 'selected')

    # Check to make sure the first part of the problem was correctly selected.
    if not isinstance(problem_data[-1][-1], tuple):
        return False
    index = (-1, -1)
    while True:
        # Try to get the neighbors, it is possible for premature IndexError,
        # in which case, omit the sample.
        neighbors = []
        # TODO : Check if correct neighbors to check.
        for offset in [(-1, -1), (0, -1)]:
            possible_neighbor = (index[0] + offset[0], index[1] + offset[1])
            neighbors.append(omit_invalid(possible_neighbor, problem_data))
        neighbors = list(filter(None, neighbors))
        for i, neighbor in enumerate(neighbors):
            if isinstance(neighbor, tuple):
                pass
            else:
                neighbors[i] = neighbor, 'not-selected'
        # No more neighbors, we must be done and the solution is correct!
        if not neighbors:
            return True
        best = max(neighbors)
        valid_choices = indicies(best, neighbors)
        for valid_choice in valid_choices:
            if neighbors[valid_choice][1] == 'selected':
                if valid_choice == 0:
                    index = (index[0] - 1, index[1] - 1)
                elif valid_choice == 1:
                    index = (index[0], index[1] - 1)
                break
        else:
            return False
    # Should never get here, but in a worst case situation!
    return False


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
    # TODO: Automate first parameter!
    return problems.render_problem('problems/needlemanwunsch.html',
                                   matrix=data,
                                   sequences=[first_seq,
                                              second_seq])
