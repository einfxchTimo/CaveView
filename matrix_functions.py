import math
import numpy as np

def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0], #right
        [0, 1, 0, 0], #up
        [0, 0, 1, 0], #forward
        [tx, ty, tz, 1] #position
    ])


def rotate_x(a):
    return np.array([
        [1, 0, 0, 0], #right
        [0, math.cos(a), math.sin(a), 0], #up
        [0, -math.sin(a), math.cos(a), 0], #forward
        [0, 0, 0, 1] #position
    ])


def rotate_y(a):
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0], #right
        [0, 1, 0, 0], #up
        [math.sin(a), 0, math.cos(a), 0], #forward
        [0, 0, 0, 1] #position
    ])