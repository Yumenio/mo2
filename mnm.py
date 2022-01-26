from manim import *
import itertools
import numpy as np
from utils import GetIntersections#get_intersections_between_two_vmobs

class Canvas(Scene):
  def construct(self):
    ax = Axes(x_range=[0,8,1], y_range=[0,8,1], tips=True)

    graph = ax.plot(lambda x: x**2, x_range=[0.01,4], use_smoothing=True)

    f1 = lambda x: x-0.5
    f2 = lambda x: 2*x/5
    f3 = lambda x: 10-(5*x/3)


    range = [0,8]

    r1 = ax.plot(f1, x_range = range, use_smoothing=True)
    r2 = ax.plot(f2, x_range = range, use_smoothing=True)
    r3 = ax.plot(f3, x_range = range, use_smoothing=True)

    s_a = [f1,f2,f3]
    function_intersections = self.get_np_intersections(s_a)
    print(function_intersections)
    
    inter_points = [Point(i, color=RED) for i in function_intersections]


    self.add(ax, r1,r2,r3)
    self.add(*inter_points)


  '''
  too inefficient, might delete later
  '''
  @staticmethod
  def get_brute_intersections(functions):
    gt = GetIntersections()
    
    inter = []
    for fi, fj in itertools.combinations(functions,2):
      fi_fj = gt.get_intersections_between_two_vmobs(fi,fj)
      inter.append(fi_fj[0])  # 1 points is more than enough

    return inter

  @staticmethod
  def get_np_intersections(functions, range=(0,10,0.01)):
    inter = []
    xinit, xend, step = range
    x = np.arange(xinit, xend, step)
    for fi, fj in itertools.combinations(functions,2):
      fix = np.array([fi(i) for i in x])
      fjx = np.array([fj(i) for i in x])
      idx = np.argwhere(np.diff(np.sign(fix - fjx))).flatten()  # find the intersections between the functions, all credits to stackOverflow
      print("a", idx)
      print("b", x[idx])
      print("c", fi(x[idx]))
      fi_fj = np.array([x[idx].tolist()[0], fi(x[idx]).tolist()[0], 0])  # append the point of intersection, 3rd dimension is added for compatibility with manim
      # fi_fj = [np.array([x[idx], fi(x[idx]), 0])]  # append the point of intersection, 3rd dimension is added for compatibility with manim
      inter.append(fi_fj)

    return inter

