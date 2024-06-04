import pygame as pg
import math
import sys

from gameObject import *
from gameObject import TILE_HEIGHT, TILE_WIDTH
from settings import *
from settings import TILE_HEIGHT, TILE_WIDTH
from items import Storage

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
                             "fridge" :     Building(self.game, "fridge", "sprites/fridge.png"), 
                             "shop" :       Building(self.game, "shop", "sprites/fridge.png", hitbox=pg.Vector2(2, 1), spriteRect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT))}
        
        self.generateWorld()
        
    
    def generateWorld(self):
        self.floor_layer = [[self.tile_library["wood-floor"].copy(pg.Vector2(x, y)) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        # self.building_layer = [[self.tile_library["empty"] for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        self.building_layer = [[(self.tile_library["counter"].copy(pg.Vector2(x, y)) if (x==0 or x==WORLD_WIDTH-1 or y==0 or y==WORLD_HEIGHT-1 or (x==4 and y!=1 and y!=WORLD_HEIGHT-2)) else self.tile_library["empty"]) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

        self.placeTile("shop", pg.Vector2(4, 0))
        self.placeTile("shop", pg.Vector2(4, 2))
        self.placeTile("shop", pg.Vector2(4, 4))
        self.placeTile("shop", pg.Vector2(4, 6))

        self.placeTile("shop", pg.Vector2(7, 0))
        self.placeTile("shop", pg.Vector2(7, 2))
        self.placeTile("shop", pg.Vector2(7, 4))
        self.placeTile("shop", pg.Vector2(7, 6))

        self.placeTile("shop", pg.Vector2(10, 0))
        self.placeTile("shop", pg.Vector2(10, 2))
        self.placeTile("shop", pg.Vector2(10, 4))
        self.placeTile("shop", pg.Vector2(10, 6))

        self.placeTile("shop", pg.Vector2(13, 0))
        self.placeTile("shop", pg.Vector2(13, 2))
        self.placeTile("shop", pg.Vector2(13, 4))
        self.placeTile("shop", pg.Vector2(13, 6))

    def is_legible_tile_placement(self, id:str, pos:pg.Vector2):
        tile = self.tile_library[id].copy(pos)
        for space in tile.get_spaces():
            if self.get(space.x, space.y) != self.tile_library["empty"]:
                return False
        return True

    def placeTile(self, id:str, pos:pg.Vector2):
        if not self.is_legible_tile_placement(id, pos):
            return

        tile = self.tile_library[id].copy(pos)

        for space in tile.get_spaces()[1:]:
            self.building_layer[int(space.y)][int(space.x)] = ReferenceTile(self.game, tile, space)
        self.building_layer[int(pos.y)][int(pos.x)] = tile

    def oob(self, x, y):
        return x < 0 or x >= WORLD_WIDTH or y < 0 or y >= WORLD_HEIGHT

    def get(self, x, y):
        if self.oob(x, y): return self.tile_library["empty"]
        else: return self.building_layer[int(y)][int(x)]

    def update(self):
        pass

    def draw(self):
        [[self.floor_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        [[self.building_layer[y][x].draw() for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]


class Tile(GameObject):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)):
        self.id = id
        super().__init__(game, pos, hitbox, sprite, spriteRect)
    
    def get_spaces(self):
        return sum([[pg.Vector2(self.pos.x + dx, self.pos.y + dy) for dx in range(int(self.hitbox.x))] for dy in range(int(self.hitbox.y))], [])

    def draw(self):
        self.game.world_renderer.draw_object_immediate(self)
    
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
    
    def draw(self):
        # self.game.world_renderer.draw_object(self)
        self.draw_ghost(self.pos)
    
    def copy(self, pos:pg.Vector2):
        return Building(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid)

    def draw_highlighted(self):
        highlight = self.sprite.convert_alpha()
        highlight.fill((255, 255, 255, 80))
        self.game.world_renderer.draw_object(self, highlight)
    
    def draw_ghost(self, pos:pg.Vector2):
        ghost = self.sprite.convert_alpha()
        ghost.set_alpha(128)
        self.game.world_renderer.draw_object(self, ghost, pos, 128)


class ReferenceTile(Building):
    def __init__(self, game, reference:Building, pos:pg.Vector2, hitbox:pg.Vector2=pg.Vector2(1, 1)):
        super().__init__(game, reference.id, reference.sprite, pos, pg.Vector2(1, 1), reference.spriteRect, reference.isSolid)
        self.reference = reference
    
    def draw(self):
        pass

    def draw_highlighted(self):
        self.reference.draw_highlighted()


class Shop(Building):
    pass

class Fridge(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1),
                 spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect, isSolid)
        self.storage = Storage()
        self.show_storage = False

    def interact(self):
        self.show_storage = not self.show_storage

    def copy(self, pos: pg.Vector2):
        return Fridge(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid)



class Processor(Building):
    pass
