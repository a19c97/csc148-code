# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller
    # @type _tree: Tree
    #     The tree containing all of the states and moves.
    # @type _current_tree_node: Tree
    #     The node of _tree that represents the last move and the last state.

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._tree = Tree((self._puzzle, None))
        self._current_tree_node = self._tree
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        action_split = action.split()
        if action == 'exit':
            return ('', True)
        elif action == ':SOLVE':
            self._puzzle = solve(self._puzzle)
            return (self.state(), True)
        elif action == ':SOLVE-ALL':
            return self._solve_all()
        elif action == ':UNDO':
            return self._undo()
        elif action == ':ATTEMPTS':
            return self._attempts()
        elif action_split[0] == ':HINT':
            return self._hint(action_split)
        else:
            return self._move(action)

    def _solve_all(self):
        """ A helper method for act.
        Solves a game and returns all of the solutions for the puzzle as a list.

        @type self: Controller
        @rtype: (str, bool)
        """
        solutions = solve_complete(self._puzzle)
        str_solutions = []
        for solution in solutions:
            str_solutions.append(str(solution))
        states = '\n'.join(str_solutions)
        return (states, True)

    def _move(self, action):
        """A helper method for act. Makes a valid move in the game and returns the new state,
        or returns an error message, if the move is invalid.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        try:
            for subtree in self._current_tree_node.subtrees:
                if subtree.root[1] == action:
                    self._current_tree_node = subtree
                    return (subtree.root[0], False)

            new_state = self._current_tree_node.root[0].move(action)
            new_tree = Tree((new_state, action))
            self._current_tree_node.add_subtree(new_tree)
            self._current_tree_node = new_tree

            if not new_state.is_solved():
                return (new_state, False)
            else:
                return (new_state, True)
        except ValueError:
            return ('Your move is invalid', False)

    def _hint(self, action_split):
        """A helper method for act. Returns a hint or an error message
        if the request is invalid.

        @type self: Controller
        @type action_split: list[str]
        @rtype: (str, bool)
        """
        if self._is_valid_hint(action_split):
            return (hint_by_depth(self._current_tree_node.root[0], int(action_split[1])), False)
        else:
            return ('Incorrect hint request', False)

    def _is_valid_hint(self, action_split):
        """Return whether the request for a hint is valid.

        @type self: Controller
        @type action_split: list[str]
        @rtype: bool
        """
        if len(action_split) != 2:
            return False
        try:
            hint_depth = int(action_split[1])
        except ValueError:
            return False
        if not hint_depth > 0:
            return False
        return True

    def _attempts(self):
        """A helper method for act. Finds and returns all of the attempted states
        from the current state.

        @type self: Controller
        @rtype: (str, bool)
        """
        message = ''
        if len(self._current_tree_node.subtrees) == 0:
            message = 'You haven`t made any attempts from this state'
        else:
            for subtree in self._current_tree_node.subtrees:
                root = subtree.root
                message += 'Reached by: ' + root[1] + '\n' + str(root[0]) + '\n'
        return (message, False)

    def _undo(self):
        """A helper method for act. Undoes the last move in the game.

        @type self: Controller
        @rtype: (str, bool)
        """
        if self._current_tree_node.parent is not None:
            self._current_tree_node = self._current_tree_node.parent
            return (str(self._current_tree_node.root[0]), False)
        else:
            return ('You have reached the initial state of the game', False)


class Tree:
    """A recursive tree data structure, modified by keeping track of each node`s parent.
    This version of tree is created specifically for the purposes of controller, it assumes that
    values of the tree are tuples with the puzzle state and a string representation of a move.
    Also, all of its attributes are public, as they need to be accessed in controller.

     === Public Attributes ===
     @type root: o(Puzzle, str | None) | None | None
         The item stored at the tree's root, or None if the tree is empty.
     @type subtrees: list[Tree]
         A list of all subtrees of the tree
     @type parent: Tree | None
         The parent tree of the current subtree or None, if tree is the root tree.
    """

    # === Representation Invariants ===
    # - If self.root is None then self._subtrees is empty.
    #   This setting of attributes represents an empty Tree.
    # - self.subtrees does not contain any empty Trees.
    # - If self.parent is None then self is the "highest order" tree.

    def __init__(self, root, parent=None):
        """Initialize a new Tree with the given root value and the given parent.

        By default, parent is None.

        If <root> is None, the tree is empty.
        A new tree always has no subtrees.

        @type self: Tree
        @type root: (Puzzle, str | None) | None
        @rtype: None
        """
        self.root = root
        self.subtrees = []
        self.parent = parent

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: Tree
        @rtype: bool
        """
        return self.root is None

    def add_subtree(self, new_tree):
        """Add the tree as a subtree of this tree.
        Only one new tree can be added at once.

        Raise ValueError if this tree is empty.

        @type self: Tree
        @type new_tree: Tree
        @rtype: None
        """
        if self.is_empty():
            raise ValueError()
        else:
            new_tree.parent = self
            self.subtrees.append(new_tree)


if __name__ == '__main__':

    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    c = Controller(s)
    from word_ladder_puzzle import WordLadderPuzzle
    w = WordLadderPuzzle('mare', 'dire')
    c = Controller(w)
