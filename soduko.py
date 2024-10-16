import bdd as bdd

def build_all_false(*a):
  if len(a) == 0:
    return bdd.Leaf.true
  return bdd.build_and(bdd.build_not(bdd.build_proposition(a[0])), build_all_false(*a[1:]))

def build_all_true(*a):
  if len(a) == 0:
    return bdd.Leaf.true
  return bdd.build_and(bdd.build_proposition(a[0]), build_all_true(*a[1:]))

def build_precisely_one(*a):
  if len(a) == 0:
    return bdd.Leaf.false
  if len(a) == 1:
    return bdd.build_proposition(a[0])
  lhs = bdd.build_and(bdd.build_proposition(a[0]), build_all_false(*a[1:]))
  rhs = bdd.build_and(bdd.build_not(bdd.build_proposition(a[0])), build_precisely_one(*a[1:]))
  return bdd.build_or(lhs, rhs)

def cell(i, j, n):
  return f"r{i}c{j}v{n}"

def cell_constraint(i, j, size):
  return build_precisely_one(*[cell(i, j, n) for n in range(1, size + 1)])

def constraints(base, block_row, block_column):
  size = block_row * block_column
  basic = base
  # Each cell has precisely one number
  print("Adding cell constraints")
  for i in range(0, size):
    for j in range(0, size):
      c = cell_constraint(i, j, size)
      basic = bdd.build_and(basic, c)
  
  constraint = bdd.Leaf.true
  for n in range(1, size + 1):
    constraint_n = basic
    print(f"Constraints for number {n}:", end="")
    # Each column has each number precisely once
    for i in range(0, size):
      print(f"c{i} ", end="", flush=True)
      c = build_precisely_one(*[cell(i, j, n) for j in range(0, size)])
      constraint_n = bdd.build_and(constraint_n, c)
    # Each row has each number precisely once
    for j in range(0, size):
      print(f"r{j} ", end="", flush=True)
      c = build_precisely_one(*[cell(i, j, n) for i in range(0, size)])
      constraint_n = bdd.build_and(constraint_n, c)
    # Each block has each number precisely once
    for bi in range(0, block_row):
      for bj in range(0, block_column):
        print(f"b{bi}{bj} ", end="", flush=True)
        c = build_precisely_one(*[cell(i, j, n) for i in range(bi * block_column, (bi + 1) * block_column) for j in range(bj * block_row, (bj + 1) * block_row)])
        constraint_n = bdd.build_and(constraint_n, c)
    constraint = bdd.build_and(constraint_n, constraint)
    print()
  return constraint

def print_assignment(constraint, size):
  curr = constraint
  i = 0
  while not isinstance(curr, bdd.Leaf):
    if curr.rhs == bdd.Leaf.false:
      # get sixth character of curr.variable.
      print(curr.variable[5], end="")
      i = i + 1
      if i % size == 0:
        print()
      curr = curr.lhs
    elif curr.lhs == bdd.Leaf.false:
      curr = curr.rhs
    else:
      print("Multiple paths")
      break

def to_cells(*strings):
  cells = []
  for i, row in enumerate(strings):
    for j, c in enumerate(row):
      if c != " ":
        cells.append(cell(i, j, int(c)))
  return cells

def solve(lines, block_row, block_column):
  size = block_row * block_column
  base = bdd.Leaf.true
  for i, row in enumerate(lines):
    for j, c in enumerate(row):
      if c != " ":
        base = bdd.build_and(base, bdd.build_proposition(cell(i, j, int(c))))
  constraint = constraints(base, block_row, block_column)
  print("================")
  print_assignment(constraint, size)
  print("================")
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
