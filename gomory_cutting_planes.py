from manim import *
import itertools
import numpy as np
from random import choice
from utils import GetIntersections#get_intersections_between_two_vmobs
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance
from input_parser import load_cp_model

# cut types
# gomoryMixedIntegerCut (may have issues with manim's interpolation, but it's more efficient)
# liftAndProject  (less efficient, but higher cut accuracy)

class Canvas(Scene):
  def construct(self):
    # ax = NumberPlane(x_length=8, y_length=8)
    ax = Axes(x_range=[0,8,1], y_range=[0,8,1], tips=True)

    # graph = ax.plot(lambda x: x**2, x_range=[0.01,4], use_smoothing=True)

    # f1 = lambda x: x-0.5
    # f2 = lambda x: 2*x/5
    # f3 = lambda x: 10-(5*x/3)



    # r1 = ax.plot(f1, x_range = range, use_smoothing=True)
    # r2 = ax.plot(f2, x_range = range, use_smoothing=True)
    # r3 = ax.plot(f3, x_range = range, use_smoothing=True)

    # s_a = [f1,f2,f3]
    # function_intersections = self.get_np_intersections(s_a)
    # print(function_intersections)
    
    # inter_points = [Dot(ax.coords_to_point(*i), color=GREEN) for i in function_intersections]
    # # inner_points = self.innerPoints(function_intersections)
    # # inner_dots = [Dot(ax.coords_to_point(*i), color = BLUE) for i in inner_points]
    # # self.add(*inner_dots)

    # self.add(ax, r1,r2,r3)
    # self.add(*inter_points)

    range = [-2,8]
    f, constraints, module = load_cp_model('model_cp_2.json')
    for constr in constraints:
      print('restriccion',constr)
      if isinstance(constr, tuple):
        type, intersect = constr
        if type == 'v':
          point = ax.coords_to_point(intersect, 10)
          c_ = ax.get_vertical_line(point)
          # self.play(Create())
          pass
        if type == 'h':
          c_ = ax.plot(lambda x: intersect, x_range = range, use_smoothing=True)
          # self.play(Create(c_))
      else:
        print(constr)
        c_ = ax.plot(constr, x_range = range, use_smoothing=True)
      self.play(Create(c_))

    sol, cc = cp.bnSolve(module,
          whichCuts = [(cp.liftAndProject, {})],   # this one generates some really odd cuts, and manim is buggy when interpolating those lines with too big coefficients in a small scale
          # whichCuts = [(cp.liftAndProject, {})],
          display = False, debug_print = False, use_cglp = False)
    sol_dot = Dot(ax.coords_to_point(*sol), color=RED)
    self.add(sol_dot)
    
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE, GREY_BROWN, PINK]
    for lambda_cut, vertical in self.cutToLambda(cc):
      if vertical:
        point = ax.coords_to_point(lambda_cut, 10)
        vline = ax.get_vertical_line(point)
        self.add(vline)
        vline.fade()
      else:
        cutGraph = ax.plot(lambda_cut,x_range=range,use_smoothing=True, color=choice(colors))
        self.play(Create(cutGraph))
        


  @staticmethod
  def cutToLambda(cuts, normalize = False):
    lmbs = []
    for cut in cuts:
      # the cut has the form ax+by=c
      # print(cut)
      a,b,c = cut.left.left[0], cut.left.left[1], cut.right
      vertical = False

      if normalize: # normalize the array cuz maybe the coeffs are too big and manim has an issue when interpolating the function values
        m = max([abs(a), abs(b), abs(c)])
        a, b, c = a/m, b/m, c/m

      # print(a,b,c)

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
    
  @staticmethod
  def innerPoints(intersection_points):
    points = []
    xmin = intersection_points[0][0]
    ymin = intersection_points[0][0]
    xmax = intersection_points[0][0]
    ymax = intersection_points[0][1]
    for point in intersection_points:
      xmin = point[0] if point[0] < xmin else xmin
      ymin = point[1] if point[1] < ymin else ymin
      xmax = point[0] if point[0] > xmax else xmax
      ymax = point[1] if point[1] > ymax else ymax

    xmin = int(xmin) if xmin-int(xmin) < 1e-5 else int(xmin) + 1
    xmax = int(xmax)
    ymin = int(ymin) if ymin-int(ymin) < 1e-5 else int(ymin) + 1
    ymax = int(ymax)

    for i in range(xmin, xmax, 1):
      for j in range(ymin, ymax, 1):
        points.append((i,j))

    return points

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
      fi_fj = [np.array([x[i], fi(x[i])]) for i in idx]  # append the point of intersection
      inter.extend(fi_fj)

    return inter

