from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # implement __eq__, __str__ methods
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = []
        >>> grid1 += [["#", "*", "*", "#"]]
        >>> grid1 += [["*", ".", "*", "*"]]
        >>> grid1 += [["*", "*", "*", "*"]]
        >>> grid1 += [["#", "*", "*", "#"]]
        >>> s1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = []
        >>> grid2 += [["#", "*", "*", "#"]]
        >>> grid2 += [["*", ".", "*", "*"]]
        >>> grid2 += [["*", "*", "*", "*"]]
        >>> grid2 += [["#", "*", "*", "#"]]
        >>> s2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> s1 == s2
        True
        >>> grid2[3][2] = "#"
        >>> s3 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> s1 == s3
        False
        """
        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation
        of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = []
        >>> grid += [["#", "*", "*", "#"]]
        >>> grid += [["*", ".", "*", "*"]]
        >>> grid += [["*", "*", "*", "*"]]
        >>> grid += [["#", "*", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s)
        #**#
        *.**
        ****
        #**#
        """
        result = ''
        for row in self._marker:
            for element in row:
                result += element
            result += '\n'
        return result.strip()

    def __repr__(self):
        """
        Return a str representing self that produces an equivalent
        GridPegSolitairePuzzle when evaluated in Python.

        @type self: GridPegSolitairePuzzle
        @rtype: str
        """
        return 'GridPegSolitairePuzzle({}, {})'.format(self._marker,
                                                       self._marker_set)

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]
        """
        search_result = []
        st = set()
        for row_index in range(len(self._marker)):
            for column_index in range(len(self._marker[row_index])):
                if self._marker[row_index][column_index] == '.':
                    search_result.append((row_index + 1, column_index + 1))
        for row_column in search_result:
            st.add(self._move_above(row_column[0], row_column[1]))
            st.add(self._move_under(row_column[0], row_column[1]))
            st.add(self._move_left(row_column[0], row_column[1]))
            st.add(self._move_right(row_column[0], row_column[1]))

        return [GridPegSolitairePuzzle(list(i), {"*", ".", "#"}) for i in st]

    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return True if there is exactly one "*" left,
        otherwise return False.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = []
        >>> grid += [["#", ".", ".", "#"]]
        >>> grid += [[".", ".", ".", "."]]
        >>> grid += [[".", "*", ".", "."]]
        >>> grid += [["#", ".", ".", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> s.is_solved()
        True
        >>> grid[0][1] = "*"
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> s.is_solved()
        False
        """
        count = 0
        for row in self._marker:
            for element in row:
                if element == "*":
                    count += 1
                if count >= 2:
                    return False
        return True

    # some helper methods
    def _move_above(self, row, column):
        """
        Move the peg which is above the empty position(row, column) to
        fill the empty position(row, column). And return the new grid in
        the form of tuple.
        If it's not possible, return the original self._marker tuple.

        @type self: GridPegSolitairePuzzle
        @type row: int
        @type column: int
        @rtype: tuple

        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [["*", "*", "*"]]
        >>> grid += [["#", ".", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_above(3, 2))
        (('#', '.', '#'), ('*', '.', '*'), ('#', '*', '#'))
        >>> grid = []
        >>> grid += [["#", ".", "#"]]
        >>> grid += [["*", "*", "*"]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_above(1, 2))
        (('#', '.', '#'), ('*', '*', '*'), ('#', '*', '#'))
        """
        # list of list is hard to make copy.
        marker = [tuple(i) for i in self._marker.copy()]
        row_above = row - 1
        row_above_above = row - 2
        if row_above < 1 or row_above_above < 1:
            return tuple(marker)
        elif (self._marker[row_above - 1][column - 1] == '*') and \
                (self._marker[row_above_above - 1][column - 1] == '*'):
            cur_row = list(marker[row - 1])
            cur_row[column - 1] = '*'
            tuple_current = tuple(cur_row)

            up_row = list(marker[row_above - 1])
            up_row[column - 1] = '.'
            tuple_above = tuple(up_row)

            up_up_row = list(marker[row_above_above - 1])
            up_up_row[column - 1] = '.'
            tuple_above_above = tuple(up_up_row)

            # generate the result
            marker[row_above_above - 1] = tuple_above_above
            marker[row_above - 1] = tuple_above
            marker[row - 1] = tuple_current
            return tuple(marker)
        else:
            return tuple(marker)

    def _move_under(self, row, column):
        """
        Move the peg which is under the empty position(row, column) to
        fill the empty position(row, column). And return the new grid in
        the form of tuple.
        If it's not possible, return the original self._marker tuple.

        @type self: GridPegSolitairePuzzle
        @type row: int
        @type column: int
        @rtype: tuple

        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [["*", "*", "*"]]
        >>> grid += [["#", ".", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_under(3, 2))
        (('#', '*', '#'), ('*', '*', '*'), ('#', '.', '#'))
        >>> grid = []
        >>> grid += [["#", ".", "#"]]
        >>> grid += [["*", "*", "*"]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_under(1, 2))
        (('#', '*', '#'), ('*', '.', '*'), ('#', '.', '#'))
        """
        marker = [tuple(i) for i in self._marker.copy()]
        row_under = row + 1
        row_under_under = row + 2
        if row_under > len(self._marker) or row_under_under > len(self._marker):
            return tuple(marker)
        elif (self._marker[row_under - 1][column - 1] == '*') and \
                (self._marker[row_under_under - 1][column - 1] == '*'):
            cur_row = list(marker[row - 1])
            cur_row[column - 1] = '*'
            tuple_current = tuple(cur_row)

            down_row = list(marker[row_under - 1])
            down_row[column - 1] = '.'
            tuple_under = tuple(down_row)

            down_down_row = list(marker[row_under_under - 1])
            down_down_row[column - 1] = '.'
            tuple_under_under = tuple(down_down_row)

            # generate the result
            marker[row_under_under - 1] = tuple_under_under
            marker[row_under - 1] = tuple_under
            marker[row - 1] = tuple_current
            return tuple(marker)
        else:
            return tuple(marker)

    def _move_left(self, row, column):
        """
        Move the peg which is left to the empty position(row, column) to
        fill the empty position(row, column). And return the new grid in
        the form of tuple.
        If it's not possible, return the original self._marker tuple.

        @type self: GridPegSolitairePuzzle
        @type row: int
        @type column: int
        @rtype: tuple

        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [["*", "*", "."]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_left(2, 3))
        (('#', '*', '#'), ('.', '.', '*'), ('#', '*', '#'))
        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [[".", "*", "*"]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_left(2, 1))
        (('#', '*', '#'), ('.', '*', '*'), ('#', '*', '#'))
        """
        marker = [tuple(i) for i in self._marker.copy()]
        column_left = column - 1
        column_left_left = column - 2
        if column_left < 1 or column_left_left < 1:
            return tuple(marker)
        elif (self._marker[row - 1][column_left - 1] == '*') and \
                (self._marker[row - 1][column_left_left - 1] == '*'):
            cur_row = list(marker[row - 1])
            cur_row[column - 1] = '*'
            cur_row[column_left - 1] = '.'
            cur_row[column_left_left - 1] = '.'
            tuple_current = tuple(cur_row)

            # generate the result
            marker[row - 1] = tuple_current
            return tuple(marker)
        else:
            return tuple(marker)

    def _move_right(self, row, column):
        """
        Move the peg which is right to the empty position(row, column) to
        fill the empty position(row, column). And return the new grid in
        the form of tuple.
        If it's not possible, return the original self._marker tuple.

        @type self: GridPegSolitairePuzzle
        @type row: int
        @type column: int
        @rtype: tuple

        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [["*", "*", "."]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_right(2, 3))
        (('#', '*', '#'), ('*', '*', '.'), ('#', '*', '#'))
        >>> grid = []
        >>> grid += [["#", "*", "#"]]
        >>> grid += [[".", "*", "*"]]
        >>> grid += [["#", "*", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(s._move_right(2, 1))
        (('#', '*', '#'), ('*', '.', '.'), ('#', '*', '#'))
        """
        marker = [tuple(i) for i in self._marker.copy()]
        column_right = column + 1
        column_right_right = column + 2
        if (column_right > len(self._marker[0])) or \
                (column_right_right > len(self._marker[0])):
            return tuple(marker)
        elif (self._marker[row - 1][column_right - 1] == '*') and \
                (self._marker[row - 1][column_right_right - 1] == '*'):
            cur_row = list(marker[row - 1])
            cur_row[column - 1] = '*'
            cur_row[column_right - 1] = '.'
            cur_row[column_right_right - 1] = '.'
            tuple_current = tuple(cur_row)

            # generate the result
            marker[row - 1] = tuple_current
            return tuple(marker)
        else:
            return tuple(marker)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
