## file to test random stuff with the line_search algorithm
from scipy.optimize import line_search
import numpy as np
import numdifftools as nd
import json
from sympy import *

model_json = json.load(open('model.json'))
json_vars = ' '.join(model_json['vars'])
json_constraints = model_json['constraints']
# must be two variables only
x, y = symbols(json_vars)
vars = (x, y)
obj_sym = parse_expr(model_json['func'])
obj_lambda = Lambda(vars, obj_sym)
constraints = [Lambda(vars, i) for i in json_constraints]
_ = obj_lambda(1,2)
_2 = constraints[0](1,2)
p = 0
gradient = [diff(obj_sym, var) for var in vars]
gradient = [ Lambda(vars, diff(obj_sym, var) ) for var in vars]
print(gradient)
a = 0
# line search
  # f = lambda x: (x[0])**2 - (x[1])**2
  # # f = lambda x: (x[0])**2 + (x[1])**2
  # # f = lambda x: (x[0])**2 + 3 * x[0] * x[1] + 12
  # gf = nd.Gradient(f)

  # # start_point = np.array([1.8, 1.7])
  # # search_gradient = np.array([-1.0, -1.0])

  # start_point = np.array([27, 16])
  # search_gradient = -1*gf(start_point)/10
  # # print(gf([1,3]))

  # best = start_point

  # for i in range(10):
  #   try:
  #     res = line_search(f, gf, start_point, search_gradient)
  #     start_point = start_point + res[0]*search_gradient
  #     print(start_point)
  #     best = start_point
  #   except:
  #     print('The best result was', best, 'with f(x,y)=', f(best))
  #     break
