#
#  This performs memoization of a function that takes itself as an argument
#  This allows the function to call itself recursively and still be memoized
#  This also breaks any long chains of recursion, by rerunning the function
#  if it needs a subcall that has not been memoized yet.
#
# Example of a recursive function that computes the nth Fibonacci number
#
# def fib_inner (fib, n):
#   if n < 2:
#     return n
#   return fib(n-1) + fib(n-2)
#
# fib = memoize(fib_inner)
def memoize(f):
  class NotFound(Exception):
    pass
  cache = {}
  # Function to be called recursively
  # Uses exceptions to signal that the value is not in the cache
  # and needs to be computed
  def recursive(*x):
    if x not in cache:
      worklist.append(x)
      raise NotFound()
    return cache[x]
  # Worker function that processes the worklist to handle
  # the recursive calls
  worklist = []
  def workloop():
    x = worklist.pop()
    while True:
      try:
        if (x) not in cache:
          cache[(x)] = f(recursive, *x)
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
  def helper(*x):
    # Add the value to the worklist
    worklist.append(x)
    # Process the worklist
    workloop()
    # Return the value from the cache
    return cache[x]
  return helper
