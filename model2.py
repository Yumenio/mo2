import numpy as np
from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray

s = CyClpSimplex()

x = s.addVariable('x', 2)

A = np.matrix([[-2,2],[2,-5],[5,3]])
a = np.matrix([-1,0,30])

s += A * x <= a
s += x >= 0

c = CyLPArray([1,1])
s.objective = c * x

print(s.primal())
print(s.primalVariableSolution['x'])