import pygame as pg
from .settings import TILE_SIZE
import random
from .build import sdm, shrine, Kopalnia, Tartak

class World:

    def __init__(self, population_manager, resource_manager, entities,  hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
        self.entities = entities

        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.buildings = [[None for x in range(self.grid_length_x)]for y in range(self.grid_length_y)]
        self.world = self.create_world()
        self.tiles = self.loadimag()

        self.temp_tile = None
        self.examine_tile = None
        self.resource_manager = resource_manager
        self.popman = population_manager



    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None


        self.temp_tile = None

        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)


            try:
                if self.can_place_tile(grid_pos):


                    img = self.hud.selected_tile["image"].copy()
                    img.set_alpha(100)

                    render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]



                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    rect = (((render_pos[0]+ camera.scroll.x),(render_pos[1] + camera.scroll.y)), ((render_pos[0] + TILE_SIZE + camera.scroll.x), (render_pos[1] +camera.scroll.y)), ((render_pos[0]+ TILE_SIZE + camera.scroll.x), (render_pos[1]+TILE_SIZE+camera.scroll.y)), ((render_pos[0] + camera.scroll.x), (render_pos[1]+TILE_SIZE+camera.scroll.y)))
                    self.temp_tile = {
                        "image": img,
                        "render_pos": render_pos,
                        "collision": collision,
                        "rect": rect
                    }

                    if mouse_action[0] and not collision:

                        if self.hud.selected_tile["name"] == 'SDM':
                            ent = sdm(render_pos, self.resource_manager, self.popman)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        elif self.hud.selected_tile["name"] == 'Shrine':
                            ent = shrine(render_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        elif self.hud.selected_tile["name"] == 'Kopalnia':
                            ent = Kopalnia(render_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        elif self.hud.selected_tile["name"] == 'Tartak':
                            ent = Tartak(render_pos, self.resource_manager)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                        self.hud.selected_tile = None

            except:
                pass
        else:
            try:
                grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                if self.can_place_tile(grid_pos):
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    if mouse_action[0] and (building is not None):
                        self.examine_tile = grid_pos
                        self.hud.examined_tile = building
            except:
                pass


    def draw(self, screen, camera):



        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):


                render_pos = self.world[x][y]["render_pos"]



                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile], (render_pos[0] + camera.scroll.x, render_pos[1] + camera.scroll.y))


                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image, (render_pos[0] + camera.scroll.x, render_pos[1] + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + camera.scroll.x, y + render_pos[1] + camera.scroll.y) for x, y
                                    in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)

        if self.temp_tile is not None:
            render_pos = self.temp_tile["render_pos"]
            rect = self.temp_tile["rect"]

            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), rect, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), rect, 3)

            screen.blit(self.temp_tile["image"], (render_pos[0]+camera.scroll.x, render_pos[1]+camera.scroll.y))

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
            "tile": tile,
            "collision": False if tile == "trawa" else True
        }

        return out

    def mouse_to_grid(self, x, y, scroll):
        world_x = x - scroll.x
        world_y = y - scroll.y
        grid_x = int(world_x // TILE_SIZE)
        grid_y = int(world_y // TILE_SIZE)

        return grid_x, grid_y

    def loadimag(self):

        trawa = pg.image.load("sprite/trawa.png").convert_alpha()
        skala = pg.image.load("sprite/skala.png").convert_alpha()

        return {'trawa': trawa, "skala": skala}


    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resouces_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_y)
        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False