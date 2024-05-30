import pygame as pg
import math
import sys

from gameObject import *
from settings import *

class World(GameObject):
    def __init__(self, game):
        self.game = game
        
        self.floor_layer = []
        self.building_layer = []

        self.floor_image = pg.image.load("sprites/floor_tile.png")
        self.floor_image = pg.transform.scale(self.floor_image, (TILE_WIDTH, TILE_HEIGHT))
        self.tile_library = {"empty" :      EmptyTile(self.game, "empty"),
                             "wood-floor" : Tile(self.game, "wood-floor", "sprites/floor_tile.png"),
                             "counter" :    Building(self.game, "counter", "sprites/counter.png", h=20, speight_ofs=4),
                             "fridge" :     Building(self.game, "fridge", "sprites/Fridge.png")}
        
        self.generateWorld()
    
    def generateWorld(self):
        self.floor_layer = [[self.tile_library["wood-floor"].copy(x, y) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        self.building_layer = [[(self.tile_library["counter"].copy(x, y) if (x==0 or x==WORLD_WIDTH-1 or y==0 or y==WORLD_HEIGHT-1) else self.tile_library["empty"]) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

    def update(self):
        pass

    def draw(self):
        self.debug_draw_grid()
        
        # for world_object in self.world_objects:
        #     world_object.draw()
    
    def debug_draw_grid(self):
        # floor
        [[self.floor_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        [[self.building_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

        #draw debug grid
        for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
            pg.draw.line(self.game.world_surf, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            pg.draw.line(self.game.world_surf, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


# class WorldObject(GameObject):
#     def __init__(self, game, hitbox):
#         self.game = game

#         self.rect = hitbox

#         self.sprite = None
#         self.spriteRect = pg.Rect(0, 0, hitbox.x, hitbox.y)

class Tile(GameObject):
    def __init__(self, game, id, sprite, x=0, y=0, w=PPT, h=PPT, spriteRect=pg.Rect(0, 0, PPT, PPT)):
        self.id = id
        self.x, self.y = x, y

        # temporary
        self.w, self.h = w, h

        self.spriteRect = spriteRect

        if isinstance(sprite, pg.Surface): self.sprite = sprite
        else: self.sprite = pg.transform.scale(pg.image.load(sprite), (w*PPP, h*PPP))

        self.game = game
    
    def draw(self):
        self.game.world_surf.blit(self.sprite, (self.x*TILE_WIDTH, self.y*TILE_HEIGHT))

    def copy(self, x, y):
        return Tile(self.game, self.id, self.sprite, x, y, self.w, self.h)

class EmptyTile(GameObject):
    def __init__(self, game, id):
        self.id = id
        self.x, self.y = 0, 0

    def copy(self):
        return self

class Building(Tile):
    def __init__(self, game, id, sprite, x=0, y=0, w=PPT, h=PPT, isSolid=True, speight_ofs=0):
        super().__init__(game, id, sprite, x, y, w, h)
        self.isSolid = isSolid
        self.speight_ofs = speight_ofs
    
    def draw(self):
        self.game.world_surf.blit(self.sprite, (self.x*TILE_WIDTH, self.y*TILE_HEIGHT-self.speight_ofs*PPP))
    
    def interact(self):
        print(f"wowww you interacted with the {self.id}!")
    
    def copy(self, x, y):
        return Building(self.game, self.id, self.sprite, x, y, self.w, self.h, self.isSolid, self.speight_ofs)

class Shop(Building):
    pass

class Storage(Building):
    pass

class Processor(Building):
    pass
