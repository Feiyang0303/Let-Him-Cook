import pygame as pg
import math
import sys

from settings import *

class World:
    def __init__(self, game):
        self.game = game
        self.world_objects = []

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        self.debug_draw_grid()
        
        for world_object in self.world_objects:
            world_object.draw()
    
    def debug_draw_grid(self):
        # draw debug grid
        for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
            pg.draw.line(self.game.screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            pg.draw.line(self.game.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


class WorldObject:
    def __init__(self, game) -> None:
        self.game = game
    
    def update(self):
        pass

    def draw(self):
        pass


class Tile:
    pass

class Building:
    pass

class Shop(Building):
    pass

class Storage(Building):
    pass

class Processor(Building):
    pass
