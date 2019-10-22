import numpy as np

import model


class Point:
    def __init__(self, x: np.float128 = 0., y: np.float128 = 0., z: np.float128 = 0., m: np.float128 = 0.):
        self.pos: np.ndarray = np.array([x, y, z], dtype=np.float128)
        self.vel: np.ndarray = np.array([0., 0., 0.], dtype=np.float128)
        self.acc: np.ndarray = np.array([0., 0., 0.], dtype=np.float128)
        self.mass: np.float = np.float128(m)

    def __str__(self):
        x, y, z = self.pos
        vx, vy, vz = self.vel
        ax, ay, az = self.acc
        return " ".join([
            f"{name}{value:{model.FLOAT_ALIGN}}"
            for name, value in (
                ("x:", x),
                ("y:", y),
                ("z:", z),
                ("vx:", vx),
                ("vy:", vy),
                ("vz:", vz),
                ("ax:", ax),
                ("ay:", ay),
                ("az:", az),
            )
        ])
