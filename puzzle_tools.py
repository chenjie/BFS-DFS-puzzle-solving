"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    pre_con = set()
    first_node = PuzzleNode(puzzle)
    flag = []

    def recursion(node):
        # Instead of creating global variables, I defined a nested function
        # which does the work of recursion.
        # recursion takes a parameter node, and returns the first node of
        # of this sequence, which has been already built up during the
        # process of recursion.
        if str(node.puzzle) not in pre_con:
            if node.puzzle.is_solved():
                flag.append(1)
                return node
            else:
                pre_con.add(str(node.puzzle))
                for i in node.puzzle.extensions():
                    p = recursion(PuzzleNode(i))
                    if flag == [1]:
                        p.parent = node
                        node.children = [p]
                        return node

    return recursion(first_node)


# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque
def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    queue = deque([PuzzleNode(puzzle)])
    pre_con = set()

    while len(queue) != 0:
        node = queue.popleft()

        if str(node.puzzle) not in pre_con:
            if node.puzzle.is_solved():
                return end_path(PuzzleNode(node.puzzle, None, node.parent))
            else:
                for move in node.puzzle.extensions():
                    queue.append(PuzzleNode(move, None, node))
            pre_con.add(str(node.puzzle))
        else:
            continue


# some helper functions
def end_path(node):
    """
    Build a path from the root to node, which should
    be the end of this path.

    @type node: PuzzleNode
    @rtype: PuzzleNode
    """
    current_node = node
    pre_node = node.parent
    while pre_node is not None:
        pre_node.children = [current_node]
        current_node = pre_node
        pre_node = pre_node.parent
    return current_node


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode] | None
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
