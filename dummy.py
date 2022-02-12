## file to test random stuff with the line_search algorithm
from scipy.optimize import line_search
import numpy as np
import numdifftools as nd

# f = lambda x,y : 5*x+8*y
# gf = nd.Gradient(f)

# start_point = np.array([1, f(1,1)])
# search_gradient = np.array([-1.0, -1.0])

# print(line_search(f, gf, start_point, search_gradient))




def backtrack(x0, dfx1, dfx2, t, alpha, beta, count):
    while (f(x0) - (f(x0 - t*np.array([dfx1(x0), dfx2(x0)])) + alpha * t * np.dot(np.array([dfx1(x0), dfx2(x0)]), np.array([dfx1(x0), dfx2(x0)])))) < 0:
        t *= beta
#         print("""

# ########################
# ###   iteration {}   ###
# ########################
# """.format(count))
#         print("Inequality: ",  f(x0) - (f(x0 - t*np.array([dfx1(x0), dfx2(x0)])) + alpha * t * np.dot(np.array([dfx1(x0), dfx2(x0)]), np.array([dfx1(x0), dfx2(x0)]))))
#         count += 1
    return t

# backtracking, no filduin
# alpha = 0.3
# beta = 0.8

# # f = lambda x: (x[0]**2 + 3*x[1]*x[0] + 12)
# # dfx1 = lambda x: (2*x[0] + 3*x[1])
# # dfx2 = lambda x: (3*x[0])

# f = lambda x: (x[0]**2)
# dfx1 = lambda x: (2*x[0])
# dfx2 = lambda x: (0)

# t = 1
# count = 1
# x0 = np.array([2,3])
# # dx0 = np.array([.1, 0.05])

# for k in range(100):
  # t = backtrack(x0, dfx1, dfx2, t, alpha, beta, count)
  # x0 = np.array([i + t for i in x0])
  # print('iteration', k, 'x,y=',x0)


# print("\nfinal step size :",  t)