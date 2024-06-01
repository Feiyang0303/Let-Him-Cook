import pygame as pg
import math
import sys

#item
class Item:
    def __init__(self, name, id, image=''):
        self.name = name
        self.id = id
        self.image = pg.image.load(image).convert_alpha()

    def display_item(self, screen, x, y):
        screen.blit(self.image, (x, y))


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
    def __init__(self, storage):
        self.storage = storage
        self.show_inventory = False

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory

    def draw(self, screen):
        if self.show_inventory:
            self.storage.draw(screen)
