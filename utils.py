from manim import *
from numpy.linalg import norm
"""
Author:         Elteoremadebeethoven
Date:           August 17/2019
Last update:    August 17/2019
OS:             Linux ArchLabs
Results:        ./
"""

def Range(in_val,end_val,step=1):
    return list(np.arange(in_val,end_val+step,step))

class GetIntersections:
    def get_coord_from_proportion(self,vmob,proportion):
        return vmob.point_from_proportion(proportion)

    # def get_points_from_curve(self, vmob, dx=0.005):
    def get_points_from_curve(self, vmob, dx=0.005):
        coords = []
        for point in Range(0, 1, dx):
            dot = Dot(self.get_coord_from_proportion(vmob,point))
            coords.append(dot.get_center())
        return coords

    def get_intersections_between_two_vmobs(self, vmob1, vmob2,
                                            tolerance=0.05,
                                            radius_error=0.2,
                                            use_average=True,
                                            use_first_vmob_reference=False):
        coords_1 = self.get_points_from_curve(vmob1)
        coords_2 = self.get_points_from_curve(vmob2)
        intersections = []
        for coord_1 in coords_1:
            for coord_2 in coords_2:
                distance_between_points = norm(coord_1 - coord_2)
                if use_average:
                    coord_3 = (coord_2 - coord_1) / 2
                    average_point = coord_1 + coord_3
                else:
                    if use_first_vmob_reference:
                        average_point = coord_1
                    else:
                        average_point = coord_2
                if len(intersections) > 0 and distance_between_points < tolerance:
                    last_intersection=intersections[-1]
                    distance_between_previus_point = norm(average_point - last_intersection)
                    if distance_between_previus_point > radius_error:
                        intersections.append(average_point)
                if len(intersections) == 0 and distance_between_points < tolerance:
                    intersections.append(average_point)
        return intersections


colors = [
    GRAY_A,
    GRAY_B,
    GRAY_C,
    GRAY_D,
    GRAY_E,
    BLACK,
    LIGHTER_GRAY,
    LIGHT_GRAY,
    GRAY,
    DARK_GRAY,
    DARKER_GRAY,
    BLUE_A,
    BLUE_B,
    BLUE_C,
    BLUE_D,
    BLUE_E,
    PURE_BLUE,
    BLUE,
    DARK_BLUE,
    TEAL_A,
    TEAL_B,
    TEAL_C,
    TEAL_D,
    TEAL_E,
    TEAL,
    GREEN_A,
    GREEN_B,
    GREEN_C,
    GREEN_D,
    GREEN_E,
    PURE_GREEN,
    GREEN,
    YELLOW_A,
    YELLOW_B,
    YELLOW_C,
    YELLOW_D,
    YELLOW_E,
    YELLOW,
    GOLD_A,
    GOLD_B,
    GOLD_C,
    GOLD_D,
    GOLD_E,
    GOLD,
    RED_A,
    RED_B,
    RED_C,
    RED_D,
    RED_E,
    PURE_RED,
    RED,
    MAROON_A,
    MAROON_B,
    MAROON_C,
    MAROON_D,
    MAROON_E,
    MAROON,
    PURPLE_A,
    PURPLE_B,
    PURPLE_C,
    PURPLE_D,
    PURPLE_E,
    PURPLE,
    PINK,
    LIGHT_PINK,
    ORANGE,
    LIGHT_BROWN,
    DARK_BROWN,
GRAY_BROWN
]