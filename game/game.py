import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .camera import Camera
from .hud import Hud

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.world = World(15, 15, self.width, self.height)

        self.camera = Camera(self.width, self.height)

        self.hud = Hud(self.width, self.height)


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
                    pg.quit()
                    sys.exit()

    def update(self):
        self.camera.update()
        self.hud.update()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):

                #sq = self.world.world[x][y]["cart_rect"]
                #rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
                #pg.draw.rect(self.screen, (0, 0, 255), rect, 1)


                render_pos = self.world.world[x][y]["render_pos"]

                tile = self.world.world[x][y]["tile"]

                self.screen.blit(self.world.tiles[tile], (render_pos[0] + self.camera.scroll.x, render_pos[1] + self.camera.scroll.y))


        self.hud.draw(self.screen)

        draw_text(self.screen,'fps {}'.format(round(self.clock.get_fps())),25,(0, 0, 0),(10, 10))



        pg.display.flip()