import pygame as pg
import math
import sys

class GameObject:
    def __init__(self, game) -> None:
        self.x, self.y = 0, 0
        self.sprite = None

        self.game = game
    
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
