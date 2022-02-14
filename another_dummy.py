from scipy.optimize import line_search
import numpy as np
import numdifftools as nd

x = np.array([2,3]) # The algorithm starts at x=2
r = 0.01 # Learning rate
p = 0.000001 # The precision at which the algorithm should be stopped
before_step_size = 1 #
i_max = 1000 # Maximum number of iterations
i = 0 #iteration counter
df = lambda x: 2*(x+3) #Gradient (First derivative)  of our function

f = lambda x : x*(x+6)
df = nd.Gradient(f)

while before_step_size > p and i < i_max:
    x_old = x # Stores the current value of x in x_old
    x = x - r * df(x_old) # Gradient descent
    before_step_size = abs(x - x_old) #Difference between consecutive iterations
    i = i+1 #Iteration increasing with every loop
    print("Iteration",i,"\nX value is",x) 
print("The local minimum of the given function occurs at", x)