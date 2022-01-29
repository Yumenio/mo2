from manim import *
import itertools
import numpy as np
from utils import GetIntersections#get_intersections_between_two_vmobs
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance

class Canvas(Scene):
  def construct(self):
    ax = Axes(x_range=[0,8,1], y_range=[0,8,1], tips=True)

    graph = ax.plot(lambda x: x**2, x_range=[0.01,4], use_smoothing=True)

    f1 = lambda x: x-0.5
    f2 = lambda x: 2*x/5
    f3 = lambda x: 10-(5*x/3)


    range = [-2,8]

    r1 = ax.plot(f1, x_range = range, use_smoothing=True)
    r2 = ax.plot(f2, x_range = range, use_smoothing=True)
    r3 = ax.plot(f3, x_range = range, use_smoothing=True)

    s_a = [f1,f2,f3]
    function_intersections = self.get_np_intersections(s_a)
    print(function_intersections)
    
    inter_points = [Dot(ax.coords_to_point(*i), color=GREEN) for i in function_intersections]
    

    self.add(ax, r1,r2,r3)
    self.add(*inter_points)
        
    cc = cp.bnSolve(MILPInstance(module_name = 'examples.e1'),
          whichCuts = [(cp.gomoryMixedIntegerCut, {})],
          display = False, debug_print = False, use_cglp = False)

    print(cc)

  @staticmethod
  def cutToLambda(cuts):
    print(cuts)

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
      fi_fj = [np.array([x[i], fi(x[i])]) for i in idx]  # append the point of intersection, 3rd dimension is added for compatibility with manim
      inter.extend(fi_fj)

    return inter

