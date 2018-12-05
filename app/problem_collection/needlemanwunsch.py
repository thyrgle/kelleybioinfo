from flask import request
from app import problems

NAME = "Needleman-Wunsch Algorithm"
CATEGORY = "RNA"
URL = "needlemanwunsch.html"


def validate(solution):
    pass


def compute_block(result, i, j, first_seq, second_seq):
    return max(result[i-1][j-1] + calc_weight(first_seq[i], second_seq[j]),
               result[i-1][j] - 1,
               result[i][j-1] - 1)


def calc_weight(first_char, second_char):
    if first_char == second_char:
        return 1
    else:
        return 0


def generate_problem_data(first_seq, second_seq):
    # Adjust sequence with "intial space"
    # Initialize the resulting matrix with the initial row.
    result = [list(range(0, -len(first_seq) - 1, -1))]
    # Create initial columns.
    for i in range(-1, -len(first_seq) - 1, -1):
        row = [i]
        row.extend([0]*len(second_seq))
        result.append(row)
    for i in range(1, len(second_seq) + 1):
        for j in range(1, len(first_seq) + 1):
            result[i][j] = compute_block(result, i, j,
                                         ' ' + second_seq,
                                         ' ' + first_seq)
    for index, letter in enumerate(second_seq):
        result[index + 1].insert(0, letter)
    result[0].insert(0, ' ')
    result.insert(0, list("  " + first_seq))
    return result


def content():
    first_seq = "GCATGCU"
    second_seq = "GATTACA"
    if request.method == 'POST':
        validate(request.data)
    return problems.render_problem('problems/needlemanwunsch.html',
                                   matrix=generate_problem_data(first_seq,
                                                                second_seq),
                                   sequences=[first_seq,
                                              second_seq])
