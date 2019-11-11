import numpy as np
import itertools


def Dodecahedron(edge):
    # flat_points = np.arange(0, 5, dtype=np.float128)
    # flat_points *= 2. * np.pi / 5.
    # points = np.zeros(shape=(5, 2))
    # points[:, 0] = np.cos(flat_points)
    # points[:, 1] = np.sin(flat_points)
    # # https://ru.wikipedia.org/wiki/Правильный_пятиугольник
    # R = edge*np.sqrt(10)*np.sqrt(5+np.sqrt(5))/10
    # points *= R

    # golden ratio
    fi = (1 + np.sqrt(5))/2
    scale_coeff = edge * fi / 2

    _1 = (-1, 1)
    _f = (-fi, fi)
    _i = (-1/fi, 1/fi)
    _0 = (0,)
    var_matrix = (
        (_1, _1, _1),
        (_0, _f, _i),
        (_i, _0, _f),
        (_f, _i, _0),
    )


    def mult_variants(current, another):
        return (
            current_case + (another_case,)
            for current_case in current
            for another_case in another
        )

    all_cases = ()
    for var_line in var_matrix:
        line_cases = map(lambda x: (x,), var_line[0])
        for case in var_line[1:]:
            line_cases = mult_variants(line_cases, case)
        all_cases = itertools.chain(all_cases, line_cases)

    return np.array(tuple(all_cases)) * scale_coeff
