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


#inventory
class Inventory:
    #table
    ROWS = 6
    COLS = 6
    CAPACITY = ROWS * COLS
    SLOT_SIZE = 50

    def __init__(self):
        self.items = []
        for row in range(Inventory.ROWS):
            row_current = []
            for col in range(Inventory.COLS):
                row_current.append(None)  # initilize with empty space
            self.items.append(row_current)

    def append_items(self, item, row, col):
        if 0 <= row <= Inventory.ROWS and 0 <= col < Inventory.COLS:
            self.items[row][col] = item

    def draw(self, screen):
        for row in range(Inventory.ROWS):
            for col in range(Inventory.COLS):
                x = col * Inventory.SLOT_SIZE
                y = row * Inventory.SLOT_SIZE
                pg.draw.rect(screen, (255, 255, 255), (x, y, Inventory.SLOT_SIZE, Inventory.SLOT_SIZE), 3)
                if self.items[row][col]:
                    self.items[row][col].display_image(screen, x, y)


