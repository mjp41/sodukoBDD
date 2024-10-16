import bdd as bdd

def _precisely_one(*a):
  result = bdd.false
  for i, prop in enumerate(a):
    conjunct = prop
    for j, prop2 in enumerate(a):
      if i == j:
        continue
      conjunct = bdd.And(conjunct, bdd.Not(prop2))
      continue
    result = bdd.Or(result, conjunct)
  return result

def _cell(i, j, n):
  return bdd.Prop(f"r{i}c{j}v{n}")

def _constraints(base, block_row, block_column):
  size = block_row * block_column
  basic = base
  # Each cell has precisely one number
  for i in range(0, size):
    for j in range(0, size):
      c = _precisely_one(*[_cell(i, j, n) for n in range(1, size + 1)])
      basic = bdd.And(basic, c)
  
  constraint = basic
  for n in range(1, size + 1):
    constraint_n = base
    print(f"{n}:", end="")
    # Each column has each number precisely once
    for i in range(0, size):
      print(f".", end="", flush=True)
      c = _precisely_one(*[_cell(i, j, n) for j in range(0, size)])
      constraint_n = bdd.And(constraint_n, c)
    # Each row has each number precisely once
    for j in range(0, size):
      print(f".", end="", flush=True)
      c = _precisely_one(*[_cell(i, j, n) for i in range(0, size)])
      constraint_n = bdd.And(constraint_n, c)
    # Each block has each number precisely once
    for bi in range(0, block_row):
      for bj in range(0, block_column):
        print(f".", end="", flush=True)
        c = _precisely_one(*[_cell(i, j, n) for i in range(bi * block_column, (bi + 1) * block_column) 
                                            for j in range(bj * block_row, (bj + 1) * block_row)])
        constraint_n = bdd.And(constraint_n, c)
    constraint = bdd.And(constraint_n, constraint)
    print()
  return constraint

def solve(lines, block_row, block_column):
  size = block_row * block_column
  base = bdd.true
  for i, row in enumerate(lines):
    for j, c in enumerate(row):
      if c != " ":
        base = bdd.And(base, _cell(i, j, int(c)))
  constraint = _constraints(base, block_row, block_column)
  print("=" * (size * 2 - 1))
  assignment = bdd.get_assignment(constraint)
  i = 0
  for i, var in enumerate(assignment):
    print(var[0][5], end=" ")
    if i % size == size - 1:
      print()
  print("=" * (size * 2 - 1))

puzzle8 = ["  8 34 6",
           " 4 312 5",
           "   7 8  ",
           "   62  7",
           "37125648",
           " 6  7 2 ",
           " 2   5 1",
           " 86147 2"]

puzzle9 = ["2  56 4  ",
           " 193     ",
           " 6       ",
           "9 4  26 5",
           "         ",
           "7 61  2 8",
           "       5 ",
           "     697 ",
           "  2 35  1"]


solve(puzzle8, 4, 2)
solve(puzzle9, 3, 3)