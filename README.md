# Python Sudoku Solver

This is Python program that solves Sudoku puzzles using backtrack algorithm.  

The implementation of algorithm is mainly based on the book **"The Algorithm Design Manual"** (Second Edition) by
Steven S. Skiena, but with following optimizations:
   1. The solver keeps a list of all open cells, each with its own set of possible numbers.
   1. Each time the solver takes the next cell having fewest possible numbers.
   1. When the solver fills a cell, it takes this cell out of the open cells list.  In addition, the solver updates
        possible values for open cells in the same affected row, column or sector.
   1. Similarly, when the solver frees a cell, it adds the cell back and updates possible values for open cells just
        like the above.

The solver takes 0.8 second to solve the hard problem in page 239 of the book.  The hard problem is also included in
the sample games.


# Requirements
Python version 3.7.3 or higher.


# Program Usage

    ./sudoku_solver.py -h
    usage: sudoku_solver.py [-h] [-s str] [-f filename] [-t]
    
    Sudoku solver using backtrack algorithm
    
    optional arguments:
      -h, --help            show this help message and exit
      -s str, --string str  a string representing a Sudoku puzzle.
      -f filename, --file filename
                            a file representing a Sudoku puzzle.
      -t, --test            runs self test on various functions, in addition to
                            solving the puzzle.
    
    Sample usage: 
    ./sudoku_solver.py -f hard
    ./sudoku_solver.py -s "041062000 000000009 090004560 700400030 020750090 000000000 007031080 083000200 004020000"

Sample output:

    ./sudoku_solver.py -f hard
    Original puzzle:
    [0, 0, 0, 0, 0, 0, 0, 1, 2]
    [0, 0, 0, 0, 3, 5, 0, 0, 0]
    [0, 0, 0, 6, 0, 0, 0, 7, 0]
    [7, 0, 0, 0, 0, 0, 3, 0, 0]
    [0, 0, 0, 4, 0, 0, 8, 0, 0]
    [1, 0, 0, 0, 0, 0, 0, 0, 0]
    [0, 0, 0, 1, 2, 0, 0, 0, 0]
    [0, 8, 0, 0, 0, 0, 0, 4, 0]
    [0, 5, 0, 0, 0, 0, 6, 0, 0]
    
    Solved puzzle:
    [6, 7, 3, 8, 9, 4, 5, 1, 2]
    [9, 1, 2, 7, 3, 5, 4, 8, 6]
    [8, 4, 5, 6, 1, 2, 9, 7, 3]
    [7, 9, 8, 2, 6, 1, 3, 5, 4]
    [5, 2, 6, 4, 7, 3, 8, 9, 1]
    [1, 3, 4, 5, 8, 9, 2, 6, 7]
    [4, 6, 9, 1, 2, 8, 7, 3, 5]
    [2, 8, 7, 3, 5, 6, 1, 4, 9]
    [3, 5, 1, 9, 4, 7, 6, 2, 8]


# Sample Games

There are 3 sample puzzles in this repo: easy, medium and hard. 

You can find more puzzles to solve at [sudoku.com](https://sudoku.com/).  Have fun!
 