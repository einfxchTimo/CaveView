from object_3d import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0, 0, -20])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('C:/Users/TimoR/Downloads/Software_3D_engine-main/resources/ti.svx')

    def get_object_from_file(self, filename):
        station = [] # [[[name, xyz Station_Punkt], ['-', xyz Leg_Punkt1], ...],                [[name, xyz Station_Punkt], ['-', xyz Leg_Punkt], ...], ...]
        with open(filename) as file:
            station.append([['Ursprung', 0, 0, 0, 1]])
            index: int = 0
            for line in file:
                args = line.split()
                höhe: float = float(args[2]) * math.sin(math.radians(float(args[4])))
                hypotenuse: float = float(args[2]) * math.cos(math.radians(float(args[4]))) #auf boden strecke
                rechts: float = hypotenuse * math.sin(math.radians(float(args[3])))
                vor: float = hypotenuse * math.cos(math.radians(float(args[3])))
                if args[1] != '-':
                    station.append([[args[1], station[index][0][1] + rechts, station[index][0][2] + höhe, station[index][0][3] + vor, 1]])
                    index = index + 1
                else:
                    station[index].append(['-', station[index][0][1] + rechts, station[index][0][2] + höhe, station[index][0][3] + vor, 1])
        return Object3D(self, station)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.object.draw()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    exit()
            self.draw()
            self.camera.control()
            pg.display.set_caption("CaveView V1.0")
            pg.display.flip()
            self.clock.tick(self.FPS)




if __name__ == '__main__':
    app = SoftwareRender()
    app.run()