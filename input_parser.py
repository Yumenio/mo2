import json
from sympy import *
import numpy as np
from coinor.cuppy.milpInstance import MILPInstance

def load_model(filepath):
  model_json = json.load(open(filepath))
  json_vars = ' '.join(model_json['vars'])
  json_constraints = model_json['constraints']
  # must be two variables only
  x, y = symbols(json_vars)
  vars = (x, y)
  obj_sym = parse_expr(model_json['func'])
  obj_lambda = Lambda(vars, obj_sym)
  constraints = [Lambda(vars, i) for i in json_constraints]
  return (vars, obj_lambda, constraints)

def load_cp_model(filepath):
  model_json = json.load(open(filepath))
  json_vars = ' '.join(model_json['vars'])
  x, y = symbols(json_vars)
  assert len(model_json['vars']) == 2, 'You must use only two variables'

  def get_cleared_constraint(ineq):
    if len(ineq.free_symbols) >= 2:
        if y in ineq.free_symbols:
            a = solve(ineq, y)
            return a.args[1]
        else:
            a = solve(ineq, x)
            return a.args[1]
    else:
        if y in ineq.free_symbols:
            a = solve(ineq, y)
            return a.args[0]
        else:
            a = solve(ineq, x)
            return a.args[0]

  def fix_single_clears(c):
    if y in c.rhs.free_symbols:
      return ('h', c.lhs)
    elif x in c.rhs.free_symbols and y not in c.lhs.free_symbols:
      return ('v', c.lhs)
    else:
      return c.rhs

  def closure_workaround(func):
    if not isinstance(func, tuple):
      return lambda x: func(x)
    else:
      return func
  
  json_constraints = [parse_expr(i) for i in model_json['constraints']]
  constraints = [get_cleared_constraint(i) for i in json_constraints]
  eq_constraints = [ fix_single_clears(i) for i in constraints]
  lambda_constraints = [Lambda(x, i) if not isinstance(i, tuple) else i for i in eq_constraints]
  lambda_constraintsf = []
  for l in lambda_constraints:
    lambda_constraintsf.append(closure_workaround(l))
  
  obj_sym = parse_expr(model_json['func'])
  obj_lambda = solve(obj_sym, y)[0]
  lmb = Lambda(x, obj_lambda)
  f = lambda t: lmb(t)
  # constraints = [Lambda(y, i) for i in cleared_constraints]

  A = np.array(model_json['A'])
  b = np.array(model_json['b'])
  c = np.array(model_json['c'])
  sense = ('Min', '<=')
  numVars = 2

  x_range = model_json['x_range']
  y_range = model_json['y_range']

  return f, lambda_constraintsf, x_range, y_range, MILPInstance(A=A, b=b, c=c, sense=sense, integerIndices=[0,1], numVars= numVars)


if __name__ == '__main__':
  x = load_cp_model('model_cp_3.json')