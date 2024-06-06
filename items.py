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
        self.game.world_renderer.draw_object(self, self.image, pos, z)
        print(pos)

#storage
class Storage:
    #table
    ROWS = 6
    COLS = 6
    CAPACITY = ROWS * COLS
    SLOT_SIZE = 50

    def __init__(self):
        self.items = []
        for row in range(Storage.ROWS):
            row_current = []
            for col in range(Storage.COLS):
                row_current.append(None)  # initilize with empty space
            self.items.append(row_current)

    def append_items(self, item, row, col):
        if 0 <= row <= Storage.ROWS and 0 <= col <Storage.COLS:
            self.items[row][col] = item

    def draw(self, screen):
        for row in range(Storage.ROWS):
            for col in range(Storage.COLS):
                x = col * Storage.SLOT_SIZE
                y = row * Storage.SLOT_SIZE
                pg.draw.rect(screen, (255, 255, 255), (x, y, Storage.SLOT_SIZE, Storage.SLOT_SIZE), 1)
                if self.items[row][col]:
                    self.items[row][col].display_item(screen, x, y)

class Inventory:
    MAX=10
    def __init__(self, game):
        self.game = game
        self.items=[]
        self.show_inventory=False

        self.item_library = {
            "sugar": Item(self.game, "sugar", "new-sprites/items/sugar.png"),
            "butter": Item(self.game, "butter", "new-sprites/items/butter.png"),
            "flour": Item(self.game, "flour", "new-sprites/items/flour.png"),
            "cookie": Item(self.game, "cookie", "new-sprites/items/cookie.png"),
        }

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory

    def add_item(self, id):
        if len(self.items)<Inventory.MAX:
            self.items.append(self.item_library[id])

    def pop(self):
        if self.items:
            return self.items.pop()

    def draw(self):
        for i, item in enumerate(self.items):
            pos = self.game.player.pos
            item.draw(pos, z=(i+1)*0.8)
