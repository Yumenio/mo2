from manim import *
import itertools
import numpy as np
from utils import GetIntersections#get_intersections_between_two_vmobs
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance

class Canvas(Scene):
  def construct(self):
    # ax = NumberPlane(x_length=8, y_length=8)
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
          # whichCuts = [(cp.gomoryMixedIntegerCut, {})],
          whichCuts = [(cp.liftAndProject, {})],
          display = False, debug_print = False, use_cglp = False)

    # self.get_vertical_line
    
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE, GREY_BROWN, PINK]
    i = 0
    for lambda_cut, vertical in self.cutToLambda(cc):
      if vertical:
        point = ax.coords_to_point(lambda_cut, 10)
        vline = ax.get_vertical_line(point)
        self.add(vline)
      else:
        print("aber corte")
        cutGraph = ax.plot(lambda_cut,x_range=range,use_smoothing=True, color=colors[i])
        self.add(cutGraph)
      i+=1


  @staticmethod
  def cutToLambda(cuts, normalize = False):
    lmbs = []
    for cut in cuts:
      # the cut has the form ax+by=c
      print(cut)
      a,b,c = cut.left.left[0], cut.left.left[1], cut.right
      vertical = False

      if normalize: # normalize the array cuz maybe the coeffs are too big and manim has an issue when interpolating the function values
        m = max([abs(a), abs(b), abs(c)])
        a, b, c = a/m, b/m, c/m

      print(a,b,c)

      # case of b = 0, vertical line
      if b == 0:
        lmb, vertical = c / a, True

      # case of a = 0, horizontal line
      elif a == 0:
        lmb = lambda x : c / b

      # case of y = (c-ax)/b
      else:
        lmb = lambda x : (c - (a * x) ) / b

      yield lmb, vertical
    


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

