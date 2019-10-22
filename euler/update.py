import numpy.linalg
import numpy as np

import model.space


class Euler:
    @staticmethod
    def update(space: model.space.Space, delta_time: np.float):
        for first in space.contains:
            first.acc = np.array([0., 0., 0.], dtype=np.float128)
            for second in space.contains:
                if first is not second:
                    delta_pos = second.pos - first.pos
                    length = numpy.linalg.norm(delta_pos)
                    first.acc += space.g_const * second.mass * delta_pos / np.float_power(length, 3)
        for instance in space.contains:
            instance.vel += instance.acc * delta_time
        for instance in space.contains:
            instance.pos += instance.vel * delta_time
        space.time += delta_time
