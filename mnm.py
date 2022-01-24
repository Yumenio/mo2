from manim import *
import itertools
from numpy import arange

class Canvas(Scene):
  def construct(self):
    ax = Axes(x_range=[0,8,1], y_range=[0,8,1], tips=True)

    graph = ax.plot(lambda x: x**2, x_range=[0.01,4], use_smoothing=True)

    f1 = lambda x: x-0.5
    f2 = lambda x: 2*x/5
    f3 = lambda x: 10-(5*x/3)

    s_a = [f1,f2,f3]

    range = [0,8]

    r1 = ax.plot(f1, x_range = range, use_smoothing=True)
    r2 = ax.plot(f2, x_range = range, use_smoothing=True)
    r3 = ax.plot(f3, x_range = range, use_smoothing=True)

    self.add(ax, r1,r2,r3)

  # @staticmethod
  # def get_intersections(functions, rang):
  #   inter = []
  #   initx, inity, step = rang, 0.01
  #   for fi, fj in itertools.combinations(functions):
  #     fi_eval = [fi(x) for x in arange(initx, inity, step)]
  #     fj_eval = [fj(x) for x in arange(initx, inity, step)]
      
