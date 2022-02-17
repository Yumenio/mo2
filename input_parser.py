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

  
  json_constraints = [parse_expr(i) for i in model_json['constraints']]
  constraints = [get_cleared_constraint(i) for i in json_constraints]
  obj_sym = parse_expr(model_json['func'])
  obj_lambda = solve(obj_sym, y)[0]
  lmb = Lambda(x, obj_lambda)
  f = lambda t: lmb(t)
  # constraints = [Lambda(y, i) for i in cleared_constraints]

  A = np.array(model_json['A'])
  b = np.array(model_json['b'])
  c = np.array(model_json['c'])
  sense = ('Max', '<=')
  numVars = 2


  return f, constraints, MILPInstance(A=A, b=b, c=c, sense=sense, integerIndices=[0,1], numVars= numVars)


if __name__ == '__main__':
  x = load_cp_model('model_cp.json')