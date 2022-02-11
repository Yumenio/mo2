## file to test random stuff with the line_search algorithm
from scipy.optimize import line_search
import numpy as np
import numdifftools as nd

f = lambda x,y : 5*x+8*y
gf = nd.Gradient(f)

start_point = np.array([1, f(1,1)])
search_gradient = np.array([-1.0, -1.0])

print(line_search(f, gf, start_point, search_gradient))