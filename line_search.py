from manim import *
import numdifftools as nd
import numpy as np
from scipy.optimize import line_search
import json
import sympy
from input_parser import load_model

class ThreeDCanvas(ThreeDScene):
  def construct(self):
    axes = ThreeDAxes()

    model_json = json.load(open('model_ls_2.json'))
    json_vars = ' '.join(model_json['vars'])
    json_constraints = model_json['constraints']
    initial_point = model_json['initial_point']
    try:
      x_range = model_json['x_range']
      y_range = model_json['y_range']
    except:
      raise Exception("You must specify the range of coordinates, i.e x_range = [-4,4], y_range = [0,10]")

    try:
      camera_phi = model_json['phi']
      camera_theta = model_json['theta']
    except:
      camera_phi = 45
      camera_theta = -120



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
          f, v_range=x_range, u_range=y_range,
          checkerboard_colors=[RED_D, RED_E], resolution=(15, 32), fill_opacity=0.5
      )


    self.set_camera_orientation(phi=camera_phi * DEGREES, theta= camera_theta * DEGREES)
    self.begin_ambient_camera_rotation(rate=0.1)

    # self.play(Rotate(c1, 0*DEGREES))
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
    assert all([constraint(initial_point[0], initial_point[1]) for constraint in constraints]), "Invalid initial point, specify one that meets all the constraints"
    
    best = start_point

    points = [best]

    threshold = 0.001
    while True:
      try:
        res = line_search(fp, gf, start_point, search_gradient)
        start_point = start_point + res[0]*search_gradient
        search_gradient = -1*gf(start_point)/2
        
        if not all([cons(start_point[0], start_point[1]) for cons in constraints]):
          break # not all constraints were TRUE
        if fp(best) - fp(start_point) < threshold:
          break # reached the threshold value, break the infinite loop
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
    opt_coords = axes.coords_to_point(*points[-1])
    ppoints.append(Dot3D(opt_coords, color=GREEN))

    txt = '(' + str( round(points[-1][0],2) ) + ',' + str( round(points[-1][1],2) ) + ',' + str( round(points[-1][2],2) ) + ')'
    dot_txt = Text(txt, font_size=20, color=PURE_GREEN)
    
    for p in ppoints:
      self.play(Rotate(p, 0*DEGREES))
    
    self.add(graph, axes)
    # self.add(dot_txt)
    # self.play(dot_txt.animate.to_edge(DOWN))
    # self.play(dot_txt.animate.to_edge(LEFT))