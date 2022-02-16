import json
from sympy import *

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
  return (obj_lambda, constraints)