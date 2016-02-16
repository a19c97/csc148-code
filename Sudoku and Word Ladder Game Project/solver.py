# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if puzzle.is_solved():
        return puzzle
    else:
        extensions = puzzle.extensions()
        if not verbose:
            for state in extensions:
                solution = solve(state)
                if solution is not None and solution.is_solved():
                    return solution
        else:
            for state in extensions:
                print(state)
                solution = solve(state, verbose)
                if solution is not None and solution.is_solved():
                    return solution
        return None


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    if puzzle.is_solved():
        return [puzzle]
    else:
        solutions = []
        extensions = puzzle.extensions()
        if not verbose:
            for state in extensions:
                solutions += solve_complete(state)
        else:
            for state in extensions:
                print(str(state))
                solutions += solve_complete(state, verbose)
        return solutions


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string 'No possible extensions!'

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    lst = _hint_by_depth_helper1(puzzle, n)
    states_at_n = lst.pop()
    for list in lst:
        for state in list:
            if state.is_solved():
                return puzzle.hint(state)
    for state in states_at_n:
        if state.is_solved():
            return puzzle.hint(state)
    if len(states_at_n) != 0:
        return puzzle.hint(states_at_n[0])
    return 'No possible extensions!'


def _hint_by_depth_helper1(puzzle, n):
    """A helper method for hint_by_depth
    Returns the list of all valid puzzle states within n moves.
    @type puzzle: Puzzle
    @type n: int
    @rtype: list[list[Puzzle]]
    """
    lst = []
    for i in range(1, n+1):
        lst.append(_hint_by_depth_helper2(puzzle, i))
    return lst


def _hint_by_depth_helper2(puzzle, n):
    """A helper function for hint_by_depth_helper1.
    Returns the list of all valid puzzle states after n moves.

    @type puzzle: Puzzle
    @type n: int
    @rtype: list[Puzzle]
    """
    extensions = puzzle.extensions()
    if len(extensions) == 0:
        return []
    elif n == 1:
        return extensions
    elif n > 1:
        states = []
        for state in extensions:
            states.extend(_hint_by_depth_helper2(state, n-1))
        return states

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])

    solution = solve(s)
    print(solution)
    solutions = solve_complete(s)
    for solution in solutions:
        print(solution)
