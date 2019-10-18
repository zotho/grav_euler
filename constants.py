import numpy as np

GRAVITATIONAL_CONST = np.float(6.67430) * np.power(np.float(10.), -11.)
"""Gravitational constant, m^3 * kg^-1 * s^-2"""


class EARTH:
    RADIUS = np.float(6378.1) * np.float(1000.)
    """Equatorial radius, m"""

    MASS = np.float(5.97237) * np.power(np.float(10.), 24.)
    """Mass, kg"""
