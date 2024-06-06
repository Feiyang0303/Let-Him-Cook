import pygame as pg
import math
import sys

from gameObject import *
from gameObject import TILE_HEIGHT, TILE_WIDTH
from items import TILE_HEIGHT, TILE_WIDTH
from settings import *
from items import *
from settings import TILE_HEIGHT, TILE_WIDTH

class World(GameObject):
    def __init__(self, game):
        self.game = game
        
        self.floor_layer = []
        self.building_layer = []

        self.tile_library = {"empty" :      EmptyTile(self.game, "empty"),
                             "floor" :      Tile(self.game, "floor", "new-sprites/buildings/floor.png"),
                             "counter" :    Counter(self.game, "counter", "new-sprites/buildings/counter.png", spriteRect=pg.Rect(0, -4*PPU, TILE_WIDTH, 20*PPU), price=10),
                             "fridge" :     Building(self.game, "fridge", "new-sprites/buildings/fridge.png", hitbox=pg.Vector2(2, 1), spriteRect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT), price=500), 
                             "shop" :       Shop(self.game, "shop", "new-sprites/buildings/shop.png", hitbox=pg.Vector2(2, 1), spriteRect=pg.Rect(0, -2*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT)),
                             "chopper" :    Processor(self.game, "chopper", "new-sprites/buildings/counter.png", spriteRect=pg.Rect(0, -4*PPU, TILE_WIDTH, 20*PPU), price=100),
        }
        
        self.generateWorld()
        

    
    def generateWorld(self): 
        self.floor_layer = [[self.tile_library["floor"].copy(pg.Vector2(x, y)) for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        # self.building_layer = [[self.tile_library["empty"] for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]
        self.building_layer = [[self.tile_library["empty"] for x in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)]

        self.place("shop", pg.Vector2(7, 0))

    def is_legible_tile_placement(self, id:str, pos:pg.Vector2):
        tile = self.tile_library[id].copy(pos)
        for space in tile.get_spaces():
            if self.get(space.x, space.y) != self.tile_library["empty"]:
                return False
        return True

    def place(self, id:str, pos:pg.Vector2):
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
        [[self.game.world_renderer]]
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
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect)
        self.isSolid = isSolid
        self.price = price
    
    def interact(self):
        print(f"wowww you interacted with the {self.id}!")
    
    def draw(self):
        self.game.world_renderer.draw_object(self)
    
    def copy(self, pos:pg.Vector2):
        return Building(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid, self.price)

    def draw_highlighted(self):
        highlight = self.sprite.convert_alpha()
        highlight.fill((255, 255, 255), special_flags=pg.BLEND_RGB_ADD)
        highlight.set_alpha(128)
        self.game.world_renderer.draw_object(self, highlight)
    
    def draw_ghost(self): 
        ghost = self.sprite.convert_alpha()
        ghost.set_alpha(128)
        self.game.world_renderer.draw_object(self, ghost, self.pos)


class Shop(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect, isSolid, price)
    
    def interact(self):
        super().interact()
        if self.game.state == PLAY_STATE:
            self.game.state = BUY_STATE
    
    def copy(self, pos:pg.Vector2):
        return Shop(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid, self.price)


class ReferenceTile(Building):
    def __init__(self, game, reference:Building, pos:pg.Vector2, hitbox:pg.Vector2=pg.Vector2(1, 1)):
        super().__init__(game, reference.id, reference.sprite, pos, pg.Vector2(1, 1), reference.spriteRect, reference.isSolid)
        self.reference = reference
    
    def draw(self):
        pass
    
    def interact(self):
        self.reference.interact()

    def draw_highlighted(self):
        self.reference.draw_highlighted()

class Counter(Building):
    def __init__(self, game, id, sprite, pos:pg.Vector2=pg.Vector2(0, 0), hitbox:pg.Vector2=pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect, isSolid, price)
        self.item = None

    def interact(self):
        if self.item == None and not self.game.player.inventory.isEmpty():
            self.item = self.game.player.inventory.next()
            self.game.player.inventory.pop()

        elif self.item != None and not self.game.player.inventory.isFull():
            self.game.player.inventory.add_item(self.item)
            self.item = None

    def draw(self):
        super().draw()
        if self.item != None:
            self.item.draw(self.pos, z=0.6)
    
    def copy(self, pos: pg.Vector2):
        return Counter(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid, self.price)


class Fridge(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1),
                 spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect, isSolid)
        self.storage = Storage()
        self.show_storage = False

    def interact(self):
        self.show_storage = not self.show_storage

    def copy(self, pos: pg.Vector2):
        return Fridge(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid, self.price)



class Processor(Building):
    def __init__(self, game, id, sprite, pos: pg.Vector2 = pg.Vector2(0, 0), hitbox: pg.Vector2 = pg.Vector2(1, 1), spriteRect=pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), isSolid=True, price=100):
        super().__init__(game, id, sprite, pos, hitbox, spriteRect, isSolid, price)
        
        self.item = None

        self.progress = 0

        self.pps = 0.1 # process per interaction
        self.ppi = 0.2 # process per interaction

    def interact(self):
        if self.item == None and not self.game.player.inventory.isEmpty():
            self.item = self.game.player.inventory.next()
            self.game.player.inventory.pop()
            self.progress = 0

        elif self.item != None:
            if self.progress < 1:
                self.progress += self.ppi
                if self.progress >= 1:
                    self.item = self.game.player.inventory.item_library["cookie"]
            
            elif self.item != None and not self.game.player.inventory.isFull():
                self.game.player.inventory.add_item(self.item)
                self.item = None

    def update(self):
        return super().update()

    def draw(self):
        super().draw()
        if self.item != None:
            self.item.draw(self.pos, z=0.6)

            # draw the progress bar
            background_bar = pg.Surface((TILE_WIDTH, 12))
            progress_bar = pg.Surface((self.progress * TILE_WIDTH, 12))
            progress_bar.fill((0, 255, 0))

            self.game.world_renderer.draw_object(self, background_bar, self.pos, z=0.5)
            self.game.world_renderer.draw_object(self, progress_bar, self.pos, z=0.5)

    
    def copy(self, pos: pg.Vector2):
        return Processor(self.game, self.id, self.sprite, pos, self.hitbox, self.spriteRect, self.isSolid, self.price)
