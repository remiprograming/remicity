import pygame as pg
from game.game import Game
from game.menu import StartMenu, GameMenu


running = True




pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

start_menu = StartMenu(screen, clock)
game_menu = GameMenu(screen, clock)

game = Game(screen, clock)

while running:
    playing = start_menu.run()

    while playing:
        game.run()
        playing = game_menu.run()
