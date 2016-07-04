import operator as op

import iem


def inside(side):
    return iem.side_value(side, op.gt, op.lt)


def inside_equal(side):
    return iem.side_value(side, op.ge, op.le)


def outside(side):
    return iem.side_value(side, op.lt, op.gt)


def inside_equal(side):
    return iem.side_value(side, op.le, op.ge)


def move_inside(side):
    return iem.side_value(side, op.add, op.sub)


def move_outside(side):
    return iem.side_value(side, op.sub, op.add)
