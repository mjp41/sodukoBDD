#
#  This performs memoization of a function
#  This also breaks any long chains of recursion, by rerunning the function
#  if it needs a subcall that has not been memoized yet.
#
# Example of a recursive function that computes the nth Fibonacci number
#
# @memoize
# def fib (n):
#   if n < 2:
#     return n
#   return fib(n-1) + fib(n-2)
#
def memoize(f):
  class NotFound(Exception):
    pass
  cache = {}
  # Worker function that processes the worklist to handle
  # the recursive calls
  worklist = []
  def workloop():
    x = worklist.pop()
    while True:
      try:
        if (x) not in cache:
          cache[(x)] = f(*x)
      except NotFound:
        # Need to compute the value on the top of the worklist
        n = worklist.pop()
        # Push the current value back on the worklist
        # until the required value is computed
        worklist.append(x)
        x = n
        continue
      # If the worklist is empty, we are done
      if len(worklist) == 0:
        break
      # Otherwise, pop the next value from the worklist
      x = worklist.pop()
  running = False
  def helper(*x):
    nonlocal running
    if running:
      # If function is called recursively
      # Uses exceptions to signal that the value is not in the cache
      # and needs to be computed
      if x not in cache:
        worklist.append(x)
        raise NotFound()
      return cache[x]
    running = True
    # Add the value to the worklist
    worklist.append(x)
    # Process the worklist
    workloop()
    # Return the value from the cache
    running = False
    return cache[x]
  return helper
