import math
import functools
from typing import List, Callable

import numpy as np

import model.point
import constants


class Space:
    def __init__(self, update: Callable[["Space", np.float], None]):
        self.g_const = constants.GRAVITATIONAL_CONST
        self.contains: List[model.point.Point] = list()
        self.time: np.float = np.float(0.)
        self.update = functools.partial(update, self)

    def add(self, instance: model.point.Point):
        self.contains.append(instance)

    def __str__(self):
        number_point_value_length = math.floor(math.log10(len(self.contains)) + 1)
        float_align = ">11.6f"
        space_description = f"Space: time: {self.time:{float_align}}"
        points_description = "\n".join([
            " ".join([f"point {number:>{number_point_value_length}}", str(instance)])
            for number, instance in enumerate(self.contains)
        ])
        return "\n".join([space_description, points_description])
