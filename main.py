from object_3d import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(0)
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('../../Downloads/Software_3D_engine-main/resources/ti.svx')

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as file:
            vertex.append([0, 0, 0, 1])
            point: list[int] = [0, 0, 0, 0] #index, x, y, z
            index: int = 0
            for line in file:
                index = index + 1
                args = line.split()
                höhe: float = float(args[2]) * math.sin(math.radians(float(args[4])))
                hypotenuse: float = float(args[2]) * math.cos(math.radians(float(args[4]))) #auf boden strecke
                rechts: float = hypotenuse * math.sin(math.radians(float(args[3])))
                vor: float = hypotenuse * math.cos(math.radians(float(args[3])))
                vertex.append([point[1] + rechts, point[2] + höhe, point[3] + vor, 1])
                #faces.append([point[0], index])
                if args[1] != '-':
                    faces.append([point[0], index])
                    point = [index, point[1] + rechts, point[2] + höhe, point[3] + vor]
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.camera.position))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()