import pygame as pg
from game.game import Game


running = True
playing = True



pg.init()
screen = pg.display.set_mode((640, 640))
clock = pg.time.Clock()

game = Game(screen, clock)

while running:

    while playing:
        game.run()
