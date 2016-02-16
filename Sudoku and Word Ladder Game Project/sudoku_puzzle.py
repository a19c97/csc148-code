# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains an uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

Note that most, but not all, of the code is given to you already.
"""
from puzzle import Puzzle
from math import sqrt

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]
        """
        chars = list(CHARS[:self._n])
        new_chars = []
        for char in chars:
            possible = True
            if char in self._grid[row_index]:
                possible = False
            for row in self._grid:
                if char == row[col_index]:
                    possible = False
            sub_grid_size = int(sqrt(self._n))
            left_col_index = int(col_index - col_index % sub_grid_size)
            top_row_index = int(row_index - row_index % sub_grid_size)
            for i in range(top_row_index, top_row_index + sub_grid_size):
                for j in range(left_col_index, left_col_index+sub_grid_size):
                    if self._grid[i][j] == char:
                        possible = False
            if possible:
                new_chars.append(char)

        return new_chars

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)

    def move(self, move):
        """ Making a move in Sudoku game. If move is invalid, raise ValueError.

        @type self: SudokuPuzzle
        @type move: str
        @rtype: SudokuPuzzle
        """
        is_valid = self.check_move(move)
        if is_valid:
            split_str = move.split()
            row_index = int(split_str[0][1:len(split_str[0])-1])
            column_index = int(split_str[1][:len(split_str[1])-1])
            new_letter = split_str[3]
            new_grid = []
            for row in self._grid:
                new_row = []
                for letter in row:
                    new_row.append(letter)
                new_grid.append(new_row)
            new_grid[row_index][column_index] = new_letter
            return SudokuPuzzle(new_grid)
        else:
            raise ValueError()

    def check_move(self, move):
        """ Returns true if the move is valid, false otherwise.
        The correct format of the move looks like this: (1, 2) -> A.
        Values of the move must also be valid, according to the rules of the game.

        @type self: SudokuPuzzle
        @type move:
        @rtype: bool
        """
        split_str = move.split()
        if len(split_str) != 4:
            return False
        if split_str[0][0] != '(' or split_str[1][len(split_str[1])-1] != ')'\
                or split_str[0][len(split_str[0])-1] != ',' or split_str[2] != '->':
            return False
        row = int(split_str[0][1:len(split_str[0])-1])
        column = int(split_str[1][:len(split_str[1])-1])
        new_letter = split_str[3]
        if row > self._n-1 or column > self._n-1 or new_letter not in CHARS[:self._n]:
            return False
        if new_letter in self._grid[row]:
            return False
        for row_in_grid in self._grid:
            if row_in_grid[column] == new_letter:
                return False
        sub_grid_size = int(sqrt(self._n))
        left_col_index = int(column - column % sub_grid_size)
        top_row_index = int(row - row % sub_grid_size)
        for i in range(top_row_index, top_row_index + sub_grid_size):
            for j in range(left_col_index, left_col_index+sub_grid_size):
                if self._grid[i][j] == new_letter:
                        return False

        return True

    def hint(self, state):
        """Implements abstract method hint. Compares self._grid
        with state._grid, returning a move string that will change the current grid
        one step closer to the state grid.

        @type self: SudokuPuzzle
        @type state: SudokuPuzzle
        @rtype: str
        """
        for i in range(self._n):
            for j in range(self._n):
                if self._grid[i][j] != state._grid[i][j]:
                    return '(' + str(i) + ', ' + str(j) + ') -> ' + state._grid[i][j]


if __name__ == '__main__':
    # Note: the doctest of 'extensions' currently fails. See Part 1.
    import doctest
    from solver import solve
    doctest.testmod()

    # Here is a bigger Sudoku puzzle
    big = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )
    print(big)
    solution = solve(big)
    print(solution)
