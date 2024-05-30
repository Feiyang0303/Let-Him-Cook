import pygame as pg
import math
import sys

class GameObject:
    def __init__(self, game) -> None:
        self.game = game

        self.rect = pg.Rect(0, 0, 0, 0)

        self.sprite = None
        self.spriteRect = pg.Rect(0, 0, 0, 0)
    
    def update(self):
        pass

    def immuneUpdate(self):
        pass
    
    def draw(self):
        pass
    
    def callEvent(self, event):
        pass

    def delete(self):
        pass
