import memo as m

class _Leaf:
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return f"{self.value}"

true = _Leaf(True)
false = _Leaf(False)

class _Node:
  def __init__(self, var, lhs, rhs):
    self.variable = var
    self.lhs = lhs
    self.rhs = rhs
  def __str__(self):
    return f"({self.variable} {self.lhs} {self.rhs})"

@m.memoize
def Prop(var):
  return _Node(var, true, false)

@m.memoize
def Not(lhs):
  if isinstance(lhs, _Leaf):
    if lhs == true:
      return false
    else:
      return true
  # Is a _Node
  return _Node(lhs.variable, Not(lhs.lhs), Not(lhs.rhs))

@m.memoize
def And(lhs, rhs):
  if (lhs == rhs):
    return lhs
  if (lhs == false) or (rhs == false):
    return false
  if (lhs == true):
    return rhs
  if (rhs == true):
    return lhs
  # Must both be _Nodes
  if lhs.variable == rhs.variable:
    new_lhs = And(lhs.lhs, rhs.lhs)
    new_rhs = And(lhs.rhs, rhs.rhs)
    var = lhs.variable
  elif lhs.variable < rhs.variable:
    new_lhs = And(lhs.lhs, rhs)
    new_rhs = And(lhs.rhs, rhs)
    var = lhs.variable
  else:
    new_lhs = And(lhs, rhs.lhs)
    new_rhs = And(lhs, rhs.rhs)
    var = rhs.variable
  ## Detect if new_lhs and new_rhs are the same
  ## Then this _Node is redundant
  if new_lhs == new_rhs:
    return new_lhs
  return _Node(var, new_lhs, new_rhs)

@m.memoize
def Or(lhs, rhs):
  if (lhs == rhs):
    return lhs
  if (lhs == true) or (rhs == true):
    return true
  if (lhs == false):
    return rhs
  if (rhs == false):
    return lhs
  # Must both be _Nodes
  if lhs.variable == rhs.variable:
    new_lhs = Or(lhs.lhs, rhs.lhs)
    new_rhs = Or(lhs.rhs, rhs.rhs)
    var = lhs.variable
  elif lhs.variable < rhs.variable:
    new_lhs = Or(lhs.lhs, rhs)
    new_rhs = Or(lhs.rhs, rhs)
    var = lhs.variable
  else:
    new_lhs = Or(lhs, rhs.lhs)
    new_rhs = Or(lhs, rhs.rhs)
    var = rhs.variable
  ## Detect if new_lhs and new_rhs are the same
  ## Then this _Node is redundant
  if new_lhs == new_rhs:
    return new_lhs
  return _Node(var, new_lhs, new_rhs)

def get_assignment(constraint):
  curr = constraint
  assignment = []
  while not isinstance(curr, _Leaf):
    if curr.rhs == false:
      assignment.append((curr.variable, True))
      curr = curr.lhs
    elif curr.lhs == false:
      curr = curr.rhs
    else:
      print("Warning: Multiple paths")
      break
  return assignment
