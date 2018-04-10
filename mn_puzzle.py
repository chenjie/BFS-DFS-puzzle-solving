from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> puzzle1 = MNPuzzle(start_grid, target_grid1)
        >>> puzzle2 = MNPuzzle(start_grid, target_grid1)
        >>> puzzle1 == puzzle2
        True
        >>> target_grid2 = (("1", "2", "3"), ("4", "*", "5"))
        >>> puzzle3 = MNPuzzle(start_grid, target_grid2)
        >>> puzzle1 == puzzle3
        False
        """
        return (type(other) == type(self) and
                (self.n, self.m) == (other.n, other.m) and
                (self.from_grid, self.to_grid) ==
                (other.from_grid, other.to_grid))

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn)
        *23
        145
        ----->
        123
        45*
        """
        result = ''
        for row in self.from_grid:
            for element in row:
                result += element
            result += '\n'
        result += '----->\n'
        for row in self.to_grid:
            for element in row:
                result += element
            result += '\n'
        return result.strip()

    def __repr__(self):
        """
        Return a str representing self that produces an equivalent
        MNPuzzle when evaluated in Python.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("*", "2"), ("3", "4"))
        >>> start_grid = (("3", "2"), ("*", "4"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn
        MNPuzzle((('3', '2'), ('*', '4')), (('*', '2'), ('3', '4')))
        """
        return 'MNPuzzle({}, {})'.format(self.from_grid, self.to_grid)

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]
        """
        row_column = []
        result = []
        for row_index in range(len(self.from_grid)):
            for column_index in range(len(self.from_grid[row_index])):
                if self.from_grid[row_index][column_index] == '*':
                    row_column = [row_index + 1, column_index + 1]
                    break
        result.append(self._move_above(row_column[0], row_column[1]))
        result.append(self._move_below(row_column[0], row_column[1]))
        result.append(self._move_left(row_column[0], row_column[1]))
        result.append(self._move_right(row_column[0], row_column[1]))

        return [i for i in result if i != self]

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return True if self.from_grid is the same as self.to_grid,
        otherwise return False.

        @type self: MNPuzzle
        @rtype: bool

        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mn1 = MNPuzzle(start_grid, target_grid1)
        >>> mn1.is_solved()
        True
        >>> target_grid2 = (("1", "2", "3"), ("4", "*", "5"))
        >>> mn2 = MNPuzzle(start_grid, target_grid2)
        >>> mn2.is_solved()
        False
        """
        return self.from_grid == self.to_grid

    # some helper methods
    def _move_above(self, row, column):
        """
        Return the new MNPuzzle in which the empty position(row, column)
        has been swapped with the number above it.
        If it's not possible, return the original MNPuzzle.

        @type self: MNPuzzle
        @type row: int
        @type column: int
        @rtype: MNPuzzle

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_above(1, 1))
        *23
        145
        ----->
        123
        45*
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("*", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_above(2, 1))
        *23
        145
        ----->
        123
        45*
        """
        row_above = row - 1
        if row_above < 1:
            return MNPuzzle(self.from_grid, self.to_grid)
        else:
            up_row = list(self.from_grid[row_above - 1])
            up_row[column - 1] = '*'
            tuple_above = tuple(up_row)

            cur_row = list(self.from_grid[row - 1])
            cur_row[column - 1] = self.from_grid[row_above - 1][column - 1]
            tuple_current = tuple(cur_row)

            # generate the result
            whole = list(self.from_grid)
            whole[row_above - 1] = tuple_above
            whole[row - 1] = tuple_current

            return MNPuzzle(tuple(whole), self.to_grid)

    def _move_below(self, row, column):
        """
        Return the new MNPuzzle in which the empty position(row, column)
        has been swapped with the number below it.
        If it's not possible, return the original MNPuzzle.

        @type self: MNPuzzle
        @type row: int
        @type column: int
        @rtype: MNPuzzle

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_below(1, 1))
        123
        *45
        ----->
        123
        45*
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("*", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_below(2, 1))
        123
        *45
        ----->
        123
        45*
        """
        row_below = row + 1
        if row_below > len(self.from_grid):
            return MNPuzzle(self.from_grid, self.to_grid)
        else:
            cur_row = list(self.from_grid[row - 1])
            cur_row[column - 1] = self.from_grid[row_below - 1][column - 1]
            tuple_current = tuple(cur_row)

            down_row = list(self.from_grid[row_below - 1])
            down_row[column - 1] = '*'
            tuple_below = tuple(down_row)

            # generate the result
            whole = list(self.from_grid)
            whole[row_below - 1] = tuple_below
            whole[row - 1] = tuple_current

            return MNPuzzle(tuple(whole), self.to_grid)

    def _move_left(self, row, column):
        """
        Return the new MNPuzzle in which the empty position(row, column)
        has been swapped with the number on its left.
        If it's not possible, return the original MNPuzzle.

        @type self: MNPuzzle
        @type row: int
        @type column: int
        @rtype: MNPuzzle

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("*", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_left(2, 1))
        123
        *45
        ----->
        123
        45*
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "*", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_left(2, 2))
        123
        *45
        ----->
        123
        45*
        """
        column_left = column - 1
        if column_left < 1:
            return MNPuzzle(self.from_grid, self.to_grid)
        else:
            cur_row = list(self.from_grid[row - 1])
            cur_row[column - 1], cur_row[column_left - 1] = \
                cur_row[column_left - 1], cur_row[column - 1]
            tuple_current = tuple(cur_row)

            # generate the result
            whole = list(self.from_grid)
            whole[row - 1] = tuple_current

            return MNPuzzle(tuple(whole), self.to_grid)

    def _move_right(self, row, column):
        """
        Return the new MNPuzzle in which the empty position(row, column)
        has been swapped with the number on its right.
        If it's not possible, return the original MNPuzzle.

        @type self: MNPuzzle
        @type row: int
        @type column: int
        @rtype: MNPuzzle

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "*", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_right(2, 2))
        123
        45*
        ----->
        123
        45*
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn._move_right(2, 3))
        123
        45*
        ----->
        123
        45*
        """
        column_right = column + 1
        if column_right > len(self.from_grid[0]):
            return MNPuzzle(self.from_grid, self.to_grid)
        else:
            cur_row = list(self.from_grid[row - 1])
            cur_row[column - 1], cur_row[column_right - 1] = \
                cur_row[column_right - 1], cur_row[column - 1]
            tuple_current = tuple(cur_row)

            # generate the result
            whole = list(self.from_grid)
            whole[row - 1] = tuple_current

            return MNPuzzle(tuple(whole), self.to_grid)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
