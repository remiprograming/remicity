import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .camera import Camera
from .hud import Hud
from .res import ResourceManager
from .pop import PopulationManager

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.entities = []

        self.resource_manager = ResourceManager()
        self.population = PopulationManager(self.resource_manager)

        self.hud = Hud(self.population, self.resource_manager, self.width, self.height)

        self.world = World(self.population, self.resource_manager, self.entities, self.hud, 10, 10, self.width, self.height)

        self.camera = Camera(self.width, self.height)




    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)
        self.population.update()
        for e in self.entities:
            e.update()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen, self.camera)

        self.hud.draw(self.screen)

        draw_text(self.screen,'fps {}'.format(round(self.clock.get_fps())),25,(0, 0, 0),(10, 10))



        pg.display.flip()