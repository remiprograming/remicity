import pygame as pg

class ResourceManager:

    def __init__(self):

        self.resources = {
            'wood': 10,
            'stone': 10,
            'chlebek': 100
        }
        self.costs = {
            'SDM': {'wood': 5, 'stone': 3},
            'Shrine': {'wood': 7, 'stone': 7},
            'Kopalnia': {'wood': 15, 'stone': 1},
            'Tartak': {'wood': 10, 'stone': 1}
        }

    def apply_cost(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable
