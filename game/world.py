import pygame as pg
from .settings import TILE_SIZE
import random

class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud

        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.world = self.create_world()
        self.tiles = self.loadimag()



    def update(self):
        pass

    def draw(self, screen, camera):

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):


                render_pos = self.world[x][y]["render_pos"]

                tile = self.world[x][y]["tile"]

                screen.blit(self.tiles[tile], (render_pos[0] + camera.scroll.x, render_pos[1] + camera.scroll.y))

    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

        return world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        minx = min([x for x, y in rect])
        miny = min([y for x, y in rect])

        r = random.randint(1,100)

        if r <= 10:
            tile = "skala"
        else:
            tile = "trawa"

        out = {
            "grid" : [grid_x, grid_y],
            "cart_rect" : rect,
            "render_pos": [minx, miny],
            "tile": tile
        }

        return out

    def loadimag(self):

        trawa = pg.image.load("sprite/trawa.png")
        skala = pg.image.load("sprite/skala.png")

        return {'trawa': trawa, "skala": skala}