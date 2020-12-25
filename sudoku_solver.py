#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from collections import namedtuple, Counter

DIMENSION = 9
NUMBERS = set(range(1, DIMENSION + 1))

Cell = namedtuple("cell", ['r', 'c'])


def main():
    args = init_param()
    board = load(args.sudoku_str)

    if args.test:
        test(board)
    else:
        if not board.is_valid():
            print('ERROR: this is not a valid Sudoku puzzle.')
            sys.exit(1)

        print(f'Original puzzle:')
        board.print_board()

        print(f'\nSolved puzzle:')
        backtrack(0, board)


class Board:
    sectors = {(0, 0): 1, (0, 1): 2, (0, 2): 3,
               (1, 0): 4, (1, 1): 5, (1, 2): 6,
               (2, 0): 7, (2, 1): 8, (2, 2): 9,
              }

    def __init__(self, matrix):
        self.m = matrix
        self.open_cells = {}
        self.get_open_cells()
        # A list to record each move, later we can use this to reconstruct the path.
        self.move = []

    def show_moves(self):
        for i, cell in enumerate(self.move):
            print('move: {:2d}, r: {}, c: {}'.format(i, cell.r, cell.c))

    def print_board(self):
        for i in self.m:
            print(i)

    def get_open_cells(self):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                if self.m[r][c] != 0:
                    continue
                cell = Cell(r, c)
                possible = possible_values(cell, self)
                # if not possible:
                #     sys.stderr.write(f'ERROR: there is no possible value for {cell}\n')
                self.open_cells[cell] = possible

    def next_square(self):
        if not self.open_cells:
            return None

        cells = sorted(self.open_cells.items(), key=lambda x: len(x[1]))
        return cells[0]

    def update_open_cells(self, cell):
        t_sector = Board.sector_id(cell)
        for i_cell in self.open_cells:
            i_sector = Board.sector_id(i_cell)
            if i_cell.r ==  cell.r or i_cell.c == cell.c or i_sector == t_sector:
                self.open_cells[i_cell] = possible_values(i_cell, self)

    def sector_filled(self, cell, filled=True):
        x = (cell.r // 3) * 3
        y = (cell.c // 3) * 3

        result = self.m[x][y:y + 3] + self.m[x + 1][y:y + 3] + self.m[x + 2][y:y + 3]
        return [num for num in result if num != 0] if filled else result

    def row(self, cell, filled=True):
        return self.m[cell.r] if not filled else [i for i in self.m[cell.r] if i != 0]

    def column(self, cell, filled=True):
        result = [self.m[i][cell.c] for i in range(DIMENSION)]
        return result if not filled else [i for i in result if i != 0]

    def valid_row(self, cell):
        nums = Counter(self.row(cell, filled=True))
        dups = list(filter(lambda x: nums[x] != 1, nums))
        if dups:
            sys.stderr.write(f'Error in row {cell.r}, duplicates found for: {list(dups)}\n')
            return False
        return True

    def valid_rows(self):
        cells = [Cell(r, 0) for r in range(DIMENSION)]
        return all(self.valid_row(cell) for cell in cells)

    def valid_column(self, cell):
        nums = Counter(self.column(cell, filled=True))
        dups = list(filter(lambda x: nums[x] != 1, nums))
        if dups:
            sys.stderr.write(f'Error in column {cell.c}, duplicates found for: {list(dups)}\n')
            return False
        return True

    def valid_columns(self):
        cells = [Cell(0, c) for c in range(DIMENSION)]
        return all(self.valid_column(cell) for cell in cells)

    def sector_id(cell):
        sector_r, sector_c = cell.r // 3, cell.c // 3
        return Board.sectors[(sector_r, sector_c)]

    def valid_sector(self, cell):
        nums = Counter(self.sector_filled(cell))
        dups = list(filter(lambda x: nums[x] != 1, nums))
        if dups:
            sector = Board.sector_id(cell)
            sys.stderr.write(f'Error in sector {sector}, duplicates found for: {list(dups)}\n')
            return False
        return True

    def valid_sectors(self):
        cells = [Cell(r, c) for r, c in Board.sectors]
        return all(self.valid_sector(cell) for cell in cells)

    def is_valid(self):
        return self.valid_rows() and self.valid_columns() and self.valid_sectors()

    def is_valid_after_kth_move(self):
        if not self.move:
            return True

        prev_cell = self.move[-1]
        return self.valid_row(prev_cell) and self.valid_column(prev_cell) and self.valid_sector(prev_cell)


def backtrack(k, board):
    valid = board.is_valid_after_kth_move()
    if not valid:
        print('ERROR: board is not valid.')
        board.show_moves()
        return

    # We've solved the puzzle.
    if not board.open_cells:
        board.print_board()
    else:
        k += 1
        cell, candidates = board.next_square()
        # print(f'cell: {cell}, candidates: {candidates}')
        if not cell or not candidates:
            return

        for num in candidates:
            fill_square(cell, num, board)
            backtrack(k, board)
            if not board.open_cells:   # for a quicker return.
                return
            free_square(cell, board)


def fill_square(cell, num, board):
    board.m[cell.r][cell.c] = num
    board.move.append(cell)
    del(board.open_cells[cell])
    board.update_open_cells(cell)


def free_square(cell, board):
    board.m[cell.r][cell.c] = 0
    board.move.pop()
    board.open_cells[cell] = set()
    board.update_open_cells(cell)


def possible_values(cell, board):
    row_nums = set(board.row(cell))
    col_nums = set(board.column(cell))
    sector_nums = set(board.sector_filled(cell))
    possible = NUMBERS - (row_nums | col_nums | sector_nums)

    return possible


def test(board):
    print('The original puzzle is:')
    board.print_board()

    cell = Cell(r=3, c=3)

    print(f'\nChecking on {cell}:')
    print(f'Numbers used in row {cell.r}: {board.row(cell)}')

    print(f'Numbers used in column {cell.c}: {board.column(cell)}')

    print(f'Numbers used in sector {Board.sector_id(cell)}: {board.sector_filled(cell)}')

    rows_valid = board.valid_rows()
    print(f'\n{rows_valid}: board rows are valid.')

    columns_valid = board.valid_columns()
    print(f'{columns_valid}: board columns are valid.')

    sectors_valid = board.valid_sectors()
    print(f'{sectors_valid}: board sectors are valid.')

    board_valid = board.is_valid()
    print(f'{board_valid}: board is valid.')

    for cell, values in board.open_cells.items():
        print(f'Open square: {cell}, possible values: {values}')

    cell, nums = board.next_square()
    print(f'\nNext square to solve: {cell}, possible numbers: {nums}')

    backtrack(0, board)

    print('\nPuzzle is solved in the below order:')
    board.show_moves()


def load(sudoku_str):
    matrix = [[0] * DIMENSION for _ in range(DIMENSION)]
    # print(f'str: {sudoku_str}')
    for i, char in enumerate(sudoku_str):
        row, col = divmod(i, DIMENSION)
        matrix[row][col] = int(char)

    return Board(matrix)


def init_param():
    sample_usage = f'Sample usage: {sys.argv[0]} -f hard'

    parser = ArgumentParser(description='Sudoku solver using backtrack algorithm', epilog=sample_usage)

    parser.add_argument('-s', '--string', metavar='str', type=str,
                        help='a string representing a Sudoku puzzle.')

    parser.add_argument('-f', '--file', metavar='filename', type=str,
                        help='a file representing a Sudoku puzzle.')

    parser.add_argument('-t', '--test', default=False, action='store_true',
                        help='runs self test on various functions, in addition to solving the puzzle.')

    args = parser.parse_args()

    sudoku_str = ""
    if args.file:
        lines = open(args.file).readlines()
        lines = [line.strip() for line in lines]
        sudoku_str = ''.join(lines)
        if ' ' in sudoku_str:
            sudoku_str = ''.join(sudoku_str.split())

    elif args.string:
        sudoku_str = args.string.replace(' ', '')

    else:
        sys.stderr.write('Please specify a puzzle using [-f file] or [-s string] option.\n')

    if len(sudoku_str) < DIMENSION * DIMENSION:
        sys.stderr.write('Error: input string needs to have 81 digits in [0-9].\n')
        sys.exit(1)

    args.sudoku_str = sudoku_str
    return args


if __name__ == '__main__':
    main()
