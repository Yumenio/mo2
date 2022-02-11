from manim import *
import itertools
import numpy as np
from random import choice
from utils import GetIntersections#get_intersections_between_two_vmobs
import coinor.cuppy.cuttingPlanes as cp
from coinor.cuppy.milpInstance import MILPInstance


class MyTestScene(Scene):
  def construct(self):
    ax = Axes(x_range=[-2,8,1], y_range=[-2,8,1], tips=True)

    # gr = ax.plot(lambda x : x, x_range=[0,2])

    gr = ax.plot(lambda x : (-599989 - (-599989*x) )/-1 , x_range= [-2,8])

    p = Dot(ax.coords_to_point(2,2), color=GREEN)



    self.add(ax, gr, p)

def buildModelFunctions(model:MILPInstance):
  A = model.A
  b = model.b
  c = model.c
  print(A,b,c)


if __name__ == "__main__":
  model = MILPInstance('examples.e2')
  lambdas = buildModelFunctions(model)
