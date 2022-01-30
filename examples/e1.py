import numpy as np

numVars = 2 #number of variables
numCons = 3 #constraints number
A = np.array([[ -2,  2],
     [  2,  -5],
     [  5,  3],
     ])
b = np.array([-1,
      0,
      30
    ])
sense = ('Min', '<=')
integerIndices = [0, 1]

c = np.array([1, 1])
obj_val = 2 

## this all doesn nothing, keeping it just in case i need it later on
  # #Rank 1 inequalities
  # cuts = [
  #     [-1.26, 2.72], 
  # #    pypolyhedron doesn't like the full-recision version 
  # #     [-1.25842697, 2.71910112], 
  #     [-2.71910112,  2.69662921],
  #     [ 2.06015038, -1.08270677], 
  #     [1, 0],
  #     [0, 1],
  #     [-1, 0],
  #     [0, -1],
  #     ]
  # rhs = [
  #     8.08,
  # #    pypolyhedron doesn't like the full-recision version 
  # #     8.08988764045,
  #     4.33707865169,
  # #     -0.563909774436,
  #     11.8496240602,
  #     7,
  #     5,
  #     -1,
  #     -1,
  #     ]

  # # This is to simulate branching
  # obj_val1 = 1.63
  # A1 = A + [[1, 0]]
  # b1 = b + [2]

  # A2 = A + [[-1, 0]]
  # b2 = b + [-3]

  # obj_val2 = 1
  # A3 = A2 + [[0, -1]]
  # b3 = b2 + [-5]

  # A4 = A2 + [[0, 1]]
  # b4 = b2 + [4]

if __name__ == '__main__':

    try:
        from coinor.cuppy.cuttingPlanes import solve, gomoryCut
        from coinor.cuppy.milpInstance import MILPInstance
    except ImportError:
        from src.cuppy.cuttingPlanes import solve, gomoryCut
        from src.cuppy.milpInstance import MILPInstance

    m = MILPInstance(A = A, b = b, c = c,
                     sense = sense, integerIndices = integerIndices,
                     numVars = numVars)
    
    solve(m, whichCuts = [(gomoryCut, {})], display = True, debug_print = True)