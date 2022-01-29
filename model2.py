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
			print(cut.right/cut.left.left[0])
			lmb = lambda x : cut.right / cut.left.left[0]

		# case of y = (c-ax)/b
		else:
			print(cut.right - cut.left.left[0],'x/',cut.left.left[1])
			lmb = lambda x : ( cut.right - ( cut.left.left[0] * x) ) / 20 #cut.left.left[1]
		
		lmbs.append(lmb)
	
	return  lmbs


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
		whichCuts = [(cp.gomoryMixedIntegerCut, {})],
		display = False, debug_print = True, use_cglp = False)

	lmb = cutsToLambda(cc)
	print(lmb)
	ys = [[lmbi(j) for j in np.arange(0,10,0.5)] for lmbi in lmb]
	print(ys)

	ll = lambda x : (-1.49999 - (-0.0 * x) ) / -1.5
	ylmb = [ ll(j) for j in np.arange(0,10,0.5)]
	print(ylmb)