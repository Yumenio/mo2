import numpy as np
from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance

s = CyClpSimplex()

x = s.addVariable('x', 2)

A = np.matrix([[-2,2],[2,-5],[5,3]])
a = np.matrix([-1,0,30])

s += A * x <= a
s += x >= 0


c = CyLPArray([1,1])
s.objective = c * x

s.primal(startFinishOptions='sfx')
print(s.primalVariableSolution['x'])

print(s.tableau)

print('aber')



            
cc = cp.bnSolve(MILPInstance(module_name = 'examples.e1'),
      whichCuts = [(cp.gomoryMixedIntegerCut, {})],
      display = False, debug_print = True, use_cglp = False)

print(cc)