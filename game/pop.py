import pygame as pg


class PopulationManager:

    def __init__(self, resource_manager):
        self.human = 100
        self.youkai = 10
        self.cap = {'human': 200, 'youkai': 50}
        self.resource_cd = pg.time.get_ticks()
        self.resource_manager = resource_manager

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cd > 1000:
            self.resource_manager.resources["chlebek"] =round(self.resource_manager.resources["chlebek"] - (0.01*self.human),2)
            if self.resource_manager.resources["chlebek"] < 0:
                self.human += round(self.resource_manager.resources["chlebek"])*2
            elif self.resource_manager.resources["chlebek"] > 0:
                if self.resource_manager.resources["chlebek"] < 100:
                    self.human += 1
                else:
                    l = self.cap['human'] - self.human
                    self.human += round(0.05*l)
            self.resource_cd = now

