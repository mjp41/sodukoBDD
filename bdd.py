import memo as m

class Leaf:
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return f"{self.value}"

Leaf.true = Leaf(True)
Leaf.false = Leaf(False)

class Node:
  def __init__(self, var, lhs, rhs):
    self.variable = var
    self.lhs = lhs
    self.rhs = rhs
  def __str__(self):
    return f"({self.variable} {self.lhs} {self.rhs})"

@m.memoize
def build_proposition(var):
  return Node(var, Leaf.true, Leaf.false)

a = build_proposition('a')

@m.memoize
def build_not(lhs):
  if isinstance(lhs, Leaf):
    if lhs == Leaf.true:
      return Leaf.false
    else:
      return Leaf.true
  # Is a Node
  return Node(lhs.variable, build_not(lhs.lhs), build_not(lhs.rhs))

na = build_not(a)

@m.memoize
def build_and(lhs, rhs):
  if (lhs == rhs):
    return lhs
  if (lhs == Leaf.false) or (rhs == Leaf.false):
    return Leaf.false
  if (lhs == Leaf.true):
    return rhs
  if (rhs == Leaf.true):
    return lhs
  # Must both be nodes
  if lhs.variable == rhs.variable:
    new_lhs = build_and(lhs.lhs, rhs.lhs)
    new_rhs = build_and(lhs.rhs, rhs.rhs)
    var = lhs.variable
  elif lhs.variable < rhs.variable:
    new_lhs = build_and(lhs.lhs, rhs)
    new_rhs = build_and(lhs.rhs, rhs)
    var = lhs.variable
  else:
    new_lhs = build_and(lhs, rhs.lhs)
    new_rhs = build_and(lhs, rhs.rhs)
    var = rhs.variable
  ## Detect if new_lhs and new_rhs are the same
  ## Then this node is redundant
  if new_lhs == new_rhs:
    return new_lhs
  return Node(var, new_lhs, new_rhs)

@m.memoize
def build_or(lhs, rhs):
  if (lhs == rhs):
    return lhs
  if (lhs == Leaf.true) or (rhs == Leaf.true):
    return Leaf.true
  if (lhs == Leaf.false):
    return rhs
  if (rhs == Leaf.false):
    return lhs
  # Must both be nodes
  if lhs.variable == rhs.variable:
    new_lhs = build_or(lhs.lhs, rhs.lhs)
    new_rhs = build_or(lhs.rhs, rhs.rhs)
    var = lhs.variable
  elif lhs.variable < rhs.variable:
    new_lhs = build_or(lhs.lhs, rhs)
    new_rhs = build_or(lhs.rhs, rhs)
    var = lhs.variable
  else:
    new_lhs = build_or(lhs, rhs.lhs)
    new_rhs = build_or(lhs, rhs.rhs)
    var = rhs.variable
  ## Detect if new_lhs and new_rhs are the same
  ## Then this node is redundant
  if new_lhs == new_rhs:
    return new_lhs
  return Node(var, new_lhs, new_rhs)