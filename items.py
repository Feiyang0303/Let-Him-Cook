import pygame as pg
import math
import sys

from settings import *
from gameObject import *

class Item(GameObject):
    def __init__(self, game, name, sprite, sellprice=1, buyprice=1):
        self.game = game
        self.name = name
        self.id = name
        self.sellprice = sellprice
        self.buyprice = buyprice
        self.sprite_rect = pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)

        if isinstance(sprite, pg.Surface): self.sprite = sprite
        else: self.sprite = pg.transform.scale(pg.image.load(sprite).convert_alpha(), (TILE_WIDTH, TILE_HEIGHT))

    def draw(self, pos, z=0):
        self.game.world_renderer.draw_object(self, self.sprite, pos, z=z)

class Package(Item):
    def __init__(self, game, name, sprite, sellprice=1, buyprice=10):
        super().__init__(game, name, sprite, sellprice, buyprice)
        self.ids = set()
    
    def check_recipe(self, building_id):
        if building_id == "counter":
            recipes = self.game.counter_recipes
        elif building_id == "oven":
            recipes = self.game.oven_recipes
        else:
            recipes = self.game.chopper_recipes

        for result, recipe in recipes.items():
            print(self.ids, set(recipe))
            if self.ids == set(recipe):
                return self.game.item_library[result]
        return self

    def add(self, item, building_id="counter"):
        self.ids.add(item.id)
        return self.check_recipe(building_id)

    def copy(self):
        return Package(self.game, self.name, self.sprite)

# storage
class Storage:
    def __init__(self, game, capacity):
        self.game = game
        self.items = []
        self.capacity = capacity

    def add(self, item):
        print("adding", item)
        if len(self.items) < self.capacity:
            if type(item) is str:
                self.items.append(self.game.item_library[item])
            else:
                self.items.append(self.game.item_library[item.id])


class Inventory:
    MAX = 10

    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.items = []
       

    def add_item(self, item):
        if len(self.items) < Inventory.MAX:
            if type(item) is str:
                self.items.append(self.game.item_library[item])
            else:
                self.items.append(self.game.item_library[item.id])

    def pop(self):
        if self.items:
            return [self.items.pop()]
        return []

    def isFull(self):
        return len(self.items) >= Inventory.MAX

    def isEmpty(self):
        return len(self.items) == 0

    def next(self):
        if len(self.items) >= 1:
            return self.items[-1]
        return None

    def draw(self):
        for i, item in enumerate(self.items):
            pos = pg.Vector2(self.player.pos.x-0.3, self.player.pos.y)
            item.draw(pos, z=(i + 3) * 0.6)
