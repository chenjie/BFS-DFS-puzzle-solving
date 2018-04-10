from puzzle import Puzzle

class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> word_set1 = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> w1 = WordLadderPuzzle("cost", "save", word_set1)
        >>> word_set2 = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> w2 = WordLadderPuzzle("cost", "save", word_set2)
        >>> w1 == w2
        True
        >>> word_set3 = {'cost', 'cast', 'case', 'cave', 'save', 'a'}
        >>> w3 = WordLadderPuzzle("cost", "save", word_set3)
        >>> w1 == w3
        False
        """
        return (type(other) == type(self) and
                ((self._from_word, self._to_word, self._word_set) ==
                 (other._from_word, other._to_word, other._word_set)))

    def __str__(self):
        """
        Return a human-readable string representation
        of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> word_set = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> w = WordLadderPuzzle("cost", "save", word_set)
        >>> print(w)
        cost -> save
        """
        return '{} -> {}'.format(self._from_word, self._to_word)

    def __repr__(self):
        """
        Return a str representing self that produces an equivalent
        WordLadderPuzzle when evaluated in Python.

        @type self: WordLadderPuzzle
        @rtype: str
        """
        return 'WordLadderPuzzle({}, {}, {})'.format(self._from_word,
                                                     self._to_word,
                                                     self._word_set)

    # override extensions
    # legal extensions are WordPadderPuzzles that have a from_word that can
    # be reached from this one by changing a single letter to one of those
    # in self._chars
    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> word_set = {'cost', 'cast', 'cbst', 'ccst', 'case', 'cave', 'save'}
        >>> w = WordLadderPuzzle("cost", "save", word_set)
        >>> print(len(w.extensions()))
        3
        """
        st = set()
        for alphabet in self._chars:
            for i in range(len(self._from_word)):
                changed_word = self._from_word[:i] + alphabet + \
                               self._from_word[i+1:]
                if (changed_word in self._word_set and
                        changed_word != self._from_word):
                    st.add(changed_word)
        result = [WordLadderPuzzle(i, self._to_word, self._word_set)
                  for i in st]
        return result

    # override is_solved
    # this WordLadderPuzzle is solved when _from_word is the same as
    # _to_word
    def is_solved(self):
        """
        Return True if self._from_word is the same as self._to_word,
        otherwise return False.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> word_set = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> w = WordLadderPuzzle("save", "save", word_set)
        >>> w.is_solved()
        True
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", 'rt', encoding='utf-8') as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
