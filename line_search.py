from manim import *
import numdifftools as nd
import numpy as np
from scipy.optimize import linesearch

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

    graph = Surface(
          lambda u, v: np.array([
              u,
              v,
              u**2+v**2
          ]), v_range=[-1, 4], u_range=[-1, 4],
          checkerboard_colors=[RED_D, RED_E], resolution=(32, 32)
      )


    self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
    self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

    self.add(axes, graph)