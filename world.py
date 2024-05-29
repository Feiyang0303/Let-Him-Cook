import pygame as pg
import math
import sys

from gameObject import *
from settings import *

class World(GameObject):
    def __init__(self, game):
        self.game = game
        self.world = []
        
        self.floor_image = pg.image.load("sprites/floor_tile.png")
        self.floor_image = pg.transform.scale(self.floor_image, (TILE_WIDTH, TILE_HEIGHT))
    
    def generateWorld(self):
        self.world = [[0]*WORLD_WIDTH for row in range(WORLD_HEIGHT)]
        self.world[10] = [1]*WORLD_WIDTH

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        self.debug_draw_grid()
        
        # for world_object in self.world_objects:
        #     world_object.draw()
    
    def debug_draw_grid(self):
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
                self.game.screen.blit(self.floor_image, (x, y))

        #draw debug grid
        for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
            pg.draw.line(self.game.screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            pg.draw.line(self.game.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))



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
