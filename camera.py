import pygame as pg

from matrix_functions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.right = np.array([1, 0, 0, 1])
        self.up = np.array([0, 1, 0, 1])
        self.forward = np.array([0, 0, 1, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.5
        self.rotation_speed = 0.015

        self.anglePitch = 0.0
        self.angleYaw = 0.0

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= np.array([math.cos(self.angleYaw), 0, -math.sin(self.angleYaw), 1]) * self.moving_speed
        if key[pg.K_d]:
            self.position += np.array([math.cos(self.angleYaw), 0, -math.sin(self.angleYaw), 1]) * self.moving_speed
        if key[pg.K_w]:
            self.position += np.array([math.sin(self.angleYaw), 0, math.cos(self.angleYaw), 1]) * self.moving_speed
        if key[pg.K_s]:
            self.position -= np.array([math.sin(self.angleYaw), 0, math.cos(self.angleYaw), 1]) * self.moving_speed
        if key[pg.K_SPACE]:
            self.position += np.array([0, 1, 0, 1]) * self.moving_speed
        if key[pg.K_LSHIFT]:
            self.position -= np.array([0, 1, 0, 1]) * self.moving_speed

        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                self.angleYaw += (800-pg.mouse.get_pos()[0])*-0.005
                if self.anglePitch > -1.5 and (450-pg.mouse.get_pos()[1])*-0.005 < 0:
                    self.anglePitch += (450-pg.mouse.get_pos()[1])*-0.005
                if self.anglePitch < 1.5 and (450-pg.mouse.get_pos()[1])*-0.005 > 0:
                    self.anglePitch += (450-pg.mouse.get_pos()[1])*-0.005
                pg.mouse.set_pos(800, 450)


    def camera_matrix(self):
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.right = np.array([1, 0, 0, 1]) @ rotate
        self.up = np.array([0, 1, 0, 1]) @ rotate
        self.forward = np.array([0, 0, 1, 1]) @ rotate
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])