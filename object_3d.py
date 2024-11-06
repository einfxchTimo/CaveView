from operator import index

import numpy as np
import pygame as pg
from matrix_functions import *
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, station=''):
        vertices, faces = [], []
        pointIndex = 0
        entryIndex = 0
        for entry in station:
            if entryIndex > 0:
                faces.append([entryIndex, pointIndex])
            entryIndex = pointIndex
            for point in entry:
                vertices.append([round(point[1], 3), round(point[2], 3), round(point[3], 3), 1])
                faces.append([entryIndex, pointIndex])
                pointIndex = pointIndex + 1

        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.vertices = self.vertices @ translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = True, False
        self.label = ''

        self.center = np.mean(self.vertices[:, :3], axis=0)
        self.radius = np.max(np.linalg.norm(self.vertices[:, :3] - self.center, axis=1))

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]


        for index, color_face in enumerate(self.color_faces):
            color, face = color_face #face: Welcher Punkt Index ist mit welchem Verbunden: [0, 2]
            if index < len(self.vertices)-1:
                self.center = self.vertices[:,:3][index]
            if self.render.camera.frustum.is_sphere_visible(self.center, 1):
                polygon = vertices[face] #Alle Bidlschirmkoordinaten der Form:[[x, y, z], ...]
                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.polygon(self.render.screen, color, polygon, 1)
                    if self.label:
                        text = self.font.render(self.label[0], True, pg.Color('white'))
                        self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices: #Für jeden Punkt der Form
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)