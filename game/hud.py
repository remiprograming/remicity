import pygame as pg
from .utils import draw_text

class Hud:
    def __init__(self, popman, resource_manager, width, height):
        self.width = width
        self.height = height
        self.hud_colour = (198, 155, 93, 175)

        self.resouces_surface = pg.Surface((width, height * 0.05), pg.SRCALPHA)
        self.resouces_rect = self.resouces_surface.get_rect(topleft=(0,0))
        self.resouces_surface.fill(self.hud_colour)


        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.hud_colour)

        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None
        self.resource_manager = resource_manager
        self.popman = popman

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    'affordable': True
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile['name']):
                tile['affordable'] = True
            else:
                tile["affordable"] = False

            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile


    def draw(self, screen):

        screen.blit(self.resouces_surface, (0,0))
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))

        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img = self.examined_tile.image.copy()
            img_scale = self.scale_image(img, h=h*0.9)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
            draw_text(screen, self.examined_tile.name, 40, (0, 0, 0), self.select_rect.topleft)

        for tile in self.tiles:
            icon = tile['icon'].copy()
            if not tile['affordable']:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

        pos = self.width - 800
        draw_text(screen, f'Ludzie: {self.popman.human}/{self.popman.cap["human"]}', 30, (0, 0, 0), (pos, 10))
        pos += 200
        draw_text(screen, f'Youkai: {self.popman.youkai}/{self.popman.cap["youkai"]}', 30, (0, 0, 0), (pos, 10))
        pos += 200
        for resource, resource_value in self.resource_manager.resources.items():
            txt = resource + ': ' + str(resource_value)
            draw_text(screen, txt, 30, (0, 0, 0), (pos, 10))
            pos += 100





    def load_images(self):

        sdm = pg.image.load("sprite/sdm.png")
        shinto = pg.image.load("sprite/shinto.png")
        kopalnia = pg.image.load("sprite/kopalnia.png")
        tartak = pg.image.load("sprite/tartak.png")

        images = {
            'SDM': sdm, 'Shrine': shinto, 'Kopalnia': kopalnia, 'Tartak': tartak
        }

        return images



    def scale_image(self, image, w=None, h=None):
        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image

