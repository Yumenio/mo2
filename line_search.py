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

    fp, constraints = load_model('model.json')

    f = lambda u,v: np.array([u,v, u**2 + 3*u*v])
    # fp = lambda x: x[0]**2 + 3*x[0]*x[1]
    constraints = []


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


    # self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
    self.set_camera_orientation(phi=45 * DEGREES, theta=-30 * DEGREES)
    self.begin_ambient_camera_rotation(rate=0.1)

    self.play(Rotate(c1, 0*DEGREES))
    self.play(Rotate(graph, 0*DEGREES))
    self.play(Rotate(axes, 0*DEGREES))

    gf = nd.Gradient(fp)
    
    start_point = np.array([3, 1.8])
    search_gradient = -1*gf(start_point)/10

    best = start_point

    points = [best]

    for _ in range(10):
      try:
        res = line_search(fp, gf, start_point, search_gradient)
        start_point = start_point + res[0]*search_gradient
        print(start_point)
        best = start_point
        points.append(best)
      except:
        print('The best result was', best, 'with f(x,y)=', fp(best))
        break

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