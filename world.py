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
                             "wood-floor" : Tile(self.game, "wood-floor", "sprites/wood-tile.png"),
                             "counter" :    Building(self.game, "counter", "sprites/e-counter.png", spriteRect=pg.Rect(0, -4*PPU, TILE_WIDTH, 20*PPU)),
                             "fridge" :     Building(self.game, "fridge", "sprites/Fridge.png")}
        
        self.generateWorld()

        self.scroll = pg.Vector2(0, WORLD_WALL_HEIGHT)
    
    def generateWorld(self):
        self.floor_layer = [[self.tile_library["wood-floor"].copy(pg.Vector2(x, y)) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        self.building_layer = [[(self.tile_library["counter"].copy(pg.Vector2(x, y)) if (x==0 or x==WORLD_WIDTH-1 or y==0 or y==WORLD_HEIGHT-1 or y==5) else self.tile_library["empty"]) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

    def oob(self, x, y):
        return x < 0 or x >= WORLD_WIDTH or y < 0 or y >= WORLD_HEIGHT

    def get(self, x, y):
        if self.oob(x, y): return self.tile_library["empty"]
        else: return self.building_layer[y][x]

    def update(self):
        pass

    def draw(self):
        self.game.world_surf.fill((255, 255, 255))
        [[self.floor_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        [[self.building_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

        # self.debug_draw_grid()
    
    def debug_draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
            pg.draw.line(self.game.world_surf, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            pg.draw.line(self.game.world_surf, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


class Tile(GameObject):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)):
        self.id = id
        super().__init__(game, pos, hitbox, sprite, spriteRect)
    
    def draw(self):
        self.game.world_surf.blit(self.sprite, ((self.pos.x + self.game.world.scroll.x)*TILE_WIDTH + self.spriteRect.x, (self.pos.y + self.game.world.scroll.y)*TILE_HEIGHT + self.spriteRect.y))

    def copy(self, pos:pg.Vector2):
        return Tile(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect)

class EmptyTile(GameObject):
    def __init__(self, game, id):
        self.game = game
        self.id = id

    def copy(self):
        return self

class Building(Tile):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect)
        self.isSolid = isSolid
    
    def interact(self):
        print(f"wowww you interacted with the {self.id}!")
    
    def copy(self, pos:pg.Vector2):
        return Building(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid)

class Shop(Building):
    pass

class Fridge(Building):
    def __init__(self):
        self.storage=Storage()
    def interact(self):
        pass

class Processor(Building):
    pass
