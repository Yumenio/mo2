import numpy as np
from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray
s = CyClpSimplex()

x = s.addVariable('x', 3)

A = np.matrix([[3,2,10],[2,4,20]])

a = np.matrix([[10],[15]])

s += A * x == a

c = CyLPArray([20,10,1])
s.objective = -1 * c * x

print(s.primal())
print(s.primalVariableSolution['x'])