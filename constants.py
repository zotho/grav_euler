import numpy as np

GRAVITATIONAL_CONST = np.float128(6.67430) * np.power(np.float128(10.), -11.)
"""Gravitational constant, m^3 * kg^-1 * s^-2"""


class EARTH:
    RADIUS = np.float128(6378.1) * np.float128(1.e3)
    """Equatorial radius, m"""

    MASS = np.float128(5.97237) * np.power(np.float128(10.), 24.)
    """Mass, kg"""

class MOON:
    """
    Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
    """
    RADIUS = np.float128(1738.1) * np.float128(1.e3)
    """Equatorial radius, m"""

    MASS = np.float128(0.07346) * np.power(np.float128(10.), 24.)
    """Mass, kg"""

    PERIGEE_ORBIT_RADIUS = np.float128(0.3633) * np.power(np.float128(10.), 9.)
    """Perigee orbit radius, m"""

    MAX_ORBITAL_VELOCITY = np.float128(1.082) * np.float128(1.e3)
    """Max. orbital velocity, m/s"""

    SYNODIC_PERIOD = np.float128(29.53) * 24. * 60. * 60.
    """Synodic period, s"""

    SIDEREAL_ROTATION_PERIOD = np.float128(655.728) * 60. * 60.
    """Sidereal rotation period, s"""
