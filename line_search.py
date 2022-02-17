from manim import *
import numdifftools as nd
import numpy as np
from scipy.optimize import line_search
import json
import sympy
from input_parser import load_model

class MyScene(ThreeDScene):
  def construct(self):
    axes = ThreeDAxes()
    # sphere = Surface(
    #       lambda u, v: np.array([
    #           1.5 * np.cos(u) * np.cos(v),
    #           1.5 * np.cos(u) * np.sin(v),
    #           1.5 * np.sin(u)
    #       ]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
    #       checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
    #   )

    # vars, fp, constraints = load_model('model.json')


    model_json = json.load(open('model.json'))
    json_vars = ' '.join(model_json['vars'])
    json_constraints = model_json['constraints']
    initial_point = model_json['initial_point']

    # must be two variables only
    x, y = sympy.symbols(json_vars)
    vars = (x, y)
    obj_sym = sympy.parse_expr(model_json['func'])
    obj_lambda = sympy.Lambda(vars, obj_sym)
    constraints = [sympy.Lambda(vars, i) for i in json_constraints]
    fp = lambda x: obj_lambda(x[0], x[1])


    f = lambda u,v: np.array([u,v, fp([u,v])])
    # fp = lambda x: x[0]**2 + 3*x[0]*x[1]
    # constraints = []


    graph = Surface(
          f, v_range=[-1, 1], u_range=[-1, 1],
          checkerboard_colors=[RED_D, RED_E], resolution=(15, 32), fill_opacity=0.5
      )



    c1 = Surface(
          lambda u, v: np.array([
              u,
              v,
              0
          ]), v_range=[-2, 2], u_range=[-2, 2],
          checkerboard_colors=[BLUE_A, BLUE_B], resolution=(15, 32),
          fill_opacity=0.3
      )


    self.set_camera_orientation(phi=45 * DEGREES, theta=-30 * DEGREES)
    self.begin_ambient_camera_rotation(rate=0.1)

    self.play(Rotate(c1, 0*DEGREES))
    self.play(Rotate(graph, 0*DEGREES))
    self.play(Rotate(axes, 0*DEGREES))

    # gf = nd.Gradient(fp)
    gradient = [ sympy.Lambda( vars, sympy.diff(obj_sym, var) ) for var in vars]
    gf = lambda x: np.array([ i(x[0],x[1]) for i in gradient ])
    # gradient = sympy.derive_by_array(fp, vars)
    print(gf([1,2]))
    print(obj_sym)
    
    start_point = np.array(initial_point)
    search_gradient = -1*gf(start_point)/10
    
    for c in constraints:
      print('testing if', c, 'holds at', initial_point, c(initial_point[0], initial_point[1]))
    assert all([constraint(initial_point[0], initial_point[1]) for constraint in constraints]), "Invalid initial point"
    
    best = start_point

    points = [best]

    for _ in range(20):
      try:
        res = line_search(fp, gf, start_point, search_gradient)
        start_point = start_point + res[0]*search_gradient
        for cons in constraints:
          if not cons(start_point[0], start_point[1]):
            break
        print(start_point)
        best = start_point
        points.append(best)
      except:
        break
        
    print('The best result was', best, 'with f(x,y)=', fp(best))

    points = [ np.array([i[0], i[1], fp(i)]) for i in points] # in ndarray form
    itt_points = [Dot3D(axes.coords_to_point(*i), color=BLUE, radius=0.07) for i in points[1:-1]] # the middle steps points
    ppoints = [Dot3D(axes.coords_to_point(*points[0]), color=RED)]
    ppoints.extend(itt_points)
    ppoints.append(Dot3D(axes.coords_to_point(*points[-1]), color=GREEN))

    print(points)
    print('oieci',DEFAULT_DOT_RADIUS)


    # self.play(Transform(graph, graph2))

    for p in ppoints:
      # self.add(p)
      self.play(Rotate(p, 0*DEGREES))
    self.add(c1, graph, axes)