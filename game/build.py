import pygame as pg

class sdm:

    def __init__(self, pos, resource_manager, popman):
        image = pg.image.load('sprite/sdm.png')
        self.image = image
        self.name = 'SDM'
        self.rect = self.image.get_rect(topleft=pos)

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost(self.name)
        self.resource_cd = pg.time.get_ticks()
        self.popman = popman
        self.popman.cap['human'] += 100
        self.popman.cap['youkai'] += 25

    def update(self):
        now = pg.time.get_ticks()



class shrine:

    def __init__(self, pos, resource_manager):
        image = pg.image.load('sprite/shinto.png')
        self.image = image
        self.name = 'Shrine'
        self.rect = self.image.get_rect(topleft=pos)

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost(self.name)
        self.resource_cd = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cd > 500:
            self.resource_manager.resources["chlebek"] += 1
            self.resource_cd = now


class Kopalnia:

    def __init__(self, pos, resource_manager):
        image = pg.image.load('sprite/kopalnia.png')
        self.image = image
        self.name = 'Kopalnia'
        self.rect = self.image.get_rect(topleft=pos)

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost(self.name)
        self.resource_cd = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cd > 2000:
            self.resource_manager.resources["stone"] += 1
            self.resource_cd = now

class Tartak:
    def __init__(self, pos, resource_manager):
        image = pg.image.load('sprite/tartak.png')
        self.image = image
        self.name = 'Tartak'
        self.rect = self.image.get_rect(topleft=pos)

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost(self.name)
        self.resource_cd = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cd > 1000:
            self.resource_manager.resources["wood"] += 1
            self.resource_cd = now


