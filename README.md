# sodukoBDD
A simple Suduko solver written in Python using ROBDDs.

This is an exercise to understand some use of state in Python.

Code structure:
* `memo.py` - A simple memoization class that can be used as a decorator to memoize functions.
  Also, break recursion by replaying the function calls.
* `bdd.py` - A simple Binary Decision Diagram implementation that uses memoization to correctly share subgraphs.
* `sudoku.py` - A simple Sudoku solver that uses the BDD implementation to solve the puzzle.