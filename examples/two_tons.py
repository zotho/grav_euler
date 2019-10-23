import math
import pathlib
import datetime

import numpy as np
import matplotlib.pyplot as plt

import model.point
import model.space
import examples
import euler.update


class TwoTons(examples.Example):
    def __init__(self):
        m = np.float128(1000.)
        r = np.float128(-10.)
        self.point_a = model.point.Point(r, m=m)
        self.point_b = model.point.Point(-r, m=m)
        self.space_instance = model.space.Space(euler.update.Euler.update)
        self.space_instance.add(self.point_a)
        self.space_instance.add(self.point_b)
        self.n_iter = 27300
        self.every = 100
        self.time_coord = np.zeros((math.floor(self.n_iter / self.every), 3))

    def run(self):
        point_a = self.point_a
        point_b = self.point_b
        space_instance = self.space_instance
        n_iter = self.n_iter
        every = self.every
        time_coord = self.time_coord
        j = 0
        for i in range(n_iter):
            space_instance.update(np.float128(10.))
            if i % every == 0:
                time_coord[j][0] = space_instance.time
                time_coord[j][1] = point_a.pos[0]
                time_coord[j][2] = point_b.pos[0]
                j += 1
                print(space_instance)
        plt.plot(time_coord[:, 0], time_coord[:, 1])
        plt.plot(time_coord[:, 0], time_coord[:, 2])
        path = pathlib.Path() / \
            "examples" / \
            "results" / \
            f"{__name__}_{str(datetime.datetime.now()).replace(' ', '_')}.png"
        while path.exists():
            path /= "_1"
        plt.savefig(path)
