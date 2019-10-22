import math

import numpy as np
import matplotlib.pyplot as plt

import model.point
import model.space
import examples
import euler.update
import constants


class EarthMoon(examples.Example):
    def __init__(self):
        self.earth = model.point.Point(m=constants.EARTH.MASS)
        self.moon = model.point.Point(constants.MOON.PERIGEE_ORBIT_RADIUS, m=constants.MOON.MASS)
        self.moon.vel[1] = constants.MOON.MAX_ORBITAL_VELOCITY
        self.earth.vel[1] = -constants.MOON.MAX_ORBITAL_VELOCITY * \
                            constants.MOON.MASS /\
                            constants.EARTH.MASS
        self.space_instance = model.space.Space(euler.update.Euler.update)
        self.space_instance.add(self.earth)
        self.space_instance.add(self.moon)
        n = 5.
        self.max_time = constants.MOON.SIDEREAL_ROTATION_PERIOD * n
        self.dt = 100. * n
        self.n_iter = math.ceil(self.max_time / self.dt)
        self.every = 100
        self.time_coord = np.zeros((math.ceil(self.n_iter / self.every), 5))

    def run(self):
        point_a = self.earth
        point_b = self.moon
        space_instance = self.space_instance
        n_iter = self.n_iter
        every = self.every
        time_coord = self.time_coord
        j = 0
        print(space_instance)
        for i in range(n_iter):
            space_instance.update(np.float128(self.dt))
            if i % every == 0:
                time_coord[j][0] = space_instance.time
                time_coord[j][1] = point_a.pos[0]
                time_coord[j][2] = point_a.pos[1]
                time_coord[j][3] = point_b.pos[0]
                time_coord[j][4] = point_b.pos[1]
                j += 1
                # print(space_instance)
        plt.plot(time_coord[:, 0], time_coord[:, 1])
        plt.plot(time_coord[:, 0], time_coord[:, 2])
        plt.plot(time_coord[:, 0], time_coord[:, 3])
        plt.plot(time_coord[:, 0], time_coord[:, 4])
        plt.show()
