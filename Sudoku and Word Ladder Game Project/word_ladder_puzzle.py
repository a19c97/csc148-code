# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""
    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _start: str
    #   The starting word of the game.
    # @type _target: str
    #   A word that should be reached by mutating the start word.
    # @type _ladder: list[str]
    #   The list of words already in the ladder.

    def __init__(self, start, target):
        """Create a new word ladder puzzle with given start and target words.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())
        # Sorting words from the dictionary, to make future search more efficient.
        self._words.sort()
        self._start = start
        self._target = target
        self._ladder = [self._start]

    def __str__(self):
        """Returns the string representation of the word ladder.

        @type self: WordLadderPuzzle
        @rtype: str
        """
        s = 'The start word is: ' + self._start
        s += '\n' + 'The target word is: ' + self._target + '\n'
        for word in self._ladder:
            s += word + '\n'

        return s

    def is_solved(self):
        """Returns whether the puzzle is solved. Word ladder is solved, when
        the last word in the ladder is the target word.

        @type self: WordLadderPuzzle
        @rtype: bool
        """
        return self._ladder[len(self._ladder)-1] == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        new_states = []
        last_word = self._ladder[len(self._ladder)-1]
        i = 0
        while i < len(last_word):
            for char in list(CHARS):
                if last_word[i] != char:
                    new_word = last_word[:i] + char + last_word[i+1:]
                    if new_word not in self._ladder:
                        # Using binary search to find a new_word in self._words
                        min_index = 0
                        max_index = len(self._words) - 1
                        while min_index <= max_index:
                            mid_index = (max_index + min_index) // 2
                            if new_word == self._words[mid_index]:
                                # Creating a copy of the ladder
                                temp = WordLadderPuzzle(self._start, self._target)
                                for word in self._ladder[1:]:
                                    temp._ladder.append(word)

                                temp._ladder.append(new_word)
                                new_states.append(temp)
                                break
                            elif new_word < self._words[mid_index]:
                                max_index = mid_index - 1
                            else:
                                min_index = mid_index + 1
            i += 1
        new_states.sort()
        return new_states

    def move(self, move):
        """Adds a word to the word ladder if the new word is a valid move.
        If not, raises ValueError.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle
        """
        is_valid = self.check_move(move)
        if is_valid:
            new_state = WordLadderPuzzle(self._start, self._target)
            for item in self._ladder[1:]:
                new_state._ladder.append(item)
            new_state._ladder.append(move)
            return new_state
        else:
            raise ValueError()

    def check_move(self, move):
        """Returns true if the move is valid, false otherwise.
        The valid move should be a string consisting of one word, and
        satisfies the rules of the game.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: bool
        """
        if not isinstance(move, str) or len(move) != len(self._start):
            return False
        if len(move.split()) != 1:
            return False
        different = 0
        last_word = self._ladder[len(self._ladder)-1]
        for i in range(len(move)):
            if move[i] != last_word[i]:
                different += 1
        if different > 1:
            return False
        if move in self._ladder:
            return False
        min_index = 0
        max_index = len(self._words) - 1
        while min_index <= max_index:
            mid_index = (max_index + min_index) // 2
            if move == self._words[mid_index]:
                return True
            elif move < self._words[mid_index]:
                max_index = mid_index - 1
            else:
                min_index = mid_index + 1
        return False

    def __lt__(self, other):
        """Returns whether the last word in the word ladder of self is less than
        the last word in the word ladder of other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool
        """
        return self._ladder[len(self._ladder)-1] < other._ladder[len(other._ladder)-1]

    def __gt__(self, other):
        """Returns whether the last word in the word ladder of self is greater than
        the last word in the word ladder of other.

        @type self: WordLadderPuzzle
        @type other:WordLadderPuzzle
        @rtype: bool
        """
        return self._ladder[len(self._ladder)-1] > other._ladder[len(other._ladder)-1]

    def hint(self, state):
        """Implementing abstract method that returns the move string that brings the
        ladder one step closer to the state ladder.

        @type self: WordLadderPuzzle
        @type state: WordLadderPuzzle
        @rtype: str
        """
        return state._ladder[len(self._ladder)]

if __name__ == '__main__':
    from solver import solve
    game = WordLadderPuzzle('mare', 'mire')
    solution = solve(game, True)
    print(solution)
