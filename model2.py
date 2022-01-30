import numpy as np
from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance

def cutsToLambda(cuts):
	print(cuts)
	lmbs = []
	for cut in cuts:
		# the cut has the form ax+by=c

		# case of b = 0
		if cut.left.left[1]==0:
			c = cut.right
			a = cut.left.left[0]
			lmb = lambda x : c / a

		# case of y = (c-ax)/b
		else:
			c = cut.right
			a = cut.left.left[0]
			b = cut.left.left[1]
			lmb = lambda x : print(a,b,c,(c-a*x)/b)
		
		lmbs.append(lmb)
	
	return  lmbs

def ycutToLambda(cuts):
    lmbs = []
    for cut in cuts:
      # the cut has the form ax+by=c

      vertical = False

      # case of b = 0
      if cut.left.left[1]==0:
        # print(cut.right/cut.left.left[0])
        lmb = lambda x : cut.right / cut.left.left[0]

      elif cut.left.left[0] == 0:
        lmb, vertical = cut.right / cut.left.left[1], True

      # case of y = (c-ax)/b
      else:
        # print(cut.right - cut.left.left[0],'x/',cut.left.left[1])
        lmb = lambda x : (cut.right - (cut.left.left[0] * x) ) / cut.left.left[1]

      yield lmb, vertical


if __name__ == '__main__':	
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
		whichCuts = [(cp.liftAndProject, {})],
		display = False, debug_print = False, use_cglp = False)


	ll = lambda x : (-1.49999 - (-0.0 * x) ) / -1.5
	for ylmb in ycutToLambda(cc):
		print(ylmb)