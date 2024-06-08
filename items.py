import pygame as pg
import math
import sys

from settings import *
from gameObject import *


class Item(GameObject):
    def __init__(self, game, name, image):
        self.game = game
        self.name = name
        self.spriteRect = pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(), (TILE_WIDTH, TILE_HEIGHT))

    def draw(self, pos, z=0):
        self.game.world_renderer.draw_object(self, self.image, pos, z=z)


# storage
class Storage:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity

    def append_items(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)


class Inventory:
    MAX = 10

    def __init__(self, game):
        self.game = game
        self.items = []
        self.show_inventory = False

        self.item_library = {
            "sugar": Item(self.game, "sugar", "new-sprites/items/sugar.png"),
            "butter": Item(self.game, "butter", "new-sprites/items/butter.png"),
            "flour": Item(self.game, "flour", "new-sprites/items/flour.png"),
            "cookie": Item(self.game, "cookie", "new-sprites/items/cookie.png"),
        }

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory

    def add_item(self, id):
        if len(self.items) < Inventory.MAX:
            self.items.append(self.item_library[id])

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
            pos = self.game.player.pos
            item.draw(pos, z=(i + 1) * 0.8)
