from manim import *

class MyTestScene(Scene):
  def construct(self):
    ax = Axes(x_range=[0,2,1], y_range=[0,2,1], tips=True)

    gr = ax.plot(lambda x : x, x_range=[0,2])

    p = Dot(ax.coords_to_point(2,2), color=GREEN)

    self.add(ax, gr, p)