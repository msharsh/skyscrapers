"""
This module works with skyscrapers game.
Git repository: https://github.com/msharsh/skyscrapers.git
"""
def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path) as board_file:
        board = board_file.readlines()
        for i in range(len(board)):
            board[i] = board[i].strip()
    return board


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    visible_buildings = 1
    max_height = input_line[1]
    for i in range(2, len(input_line)-1):
        if int(input_line[i]) > int(max_height):
            visible_buildings += 1
            max_height = int(input_line[i])
    if visible_buildings == pivot:
        return True
    return False


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for i in range(1, len(board)-1):
        line_temp = []
        for j in range(1, len(board[i])-1):
            if board[i][j] in line_temp:
                return False
            line_temp.append(board[i][j])
    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    check = True
    for i in range(1, len(board)-1):
        if board[i][0] != '*' and board[i][-1] != '*':
            check = left_to_right_check(board[i], int(board[i][0])) &\
                left_to_right_check(board[i][::-1], int(board[i][-1]))
        elif board[i][0] != '*':
            check = left_to_right_check(board[i], int(board[i][0]))
        elif board[i][-1] != '*':
            check = left_to_right_check(board[i][::-1], int(board[i][-1]))
        if not check:
            return False
    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    board_turned = []
    for i in range(len(board[0])):
        new_row = ''
        for j in range(len(board)):
            new_row += board[j][i]
        board_turned.append(new_row)
    check_uniqueness = check_uniqueness_in_rows(board_turned)
    check_visibility = check_horizontal_visibility(board_turned)
    return check_uniqueness & check_visibility


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)
    if check_not_finished_board(board) and\
        check_uniqueness_in_rows(board) and\
            check_horizontal_visibility(board) and\
                check_columns(board):
        return True
    return False


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
