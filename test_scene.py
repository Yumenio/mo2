from manim import *

class MyTestScene(Scene):
  def construct(self):
    ax = Axes(x_range=[-2,8,1], y_range=[-2,8,1], tips=True)

    # gr = ax.plot(lambda x : x, x_range=[0,2])

    gr = ax.plot(lambda x : (-599989 - (-599989*x) )/-1 , x_range= [-2,8])

    p = Dot(ax.coords_to_point(2,2), color=GREEN)

    self.add(ax, gr, p)