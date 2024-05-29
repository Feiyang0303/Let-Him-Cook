import pygame as pg
import math
import sys

from gameObject import *
from settings import *

class WorldEditor(GameObject):
    def __init__(self, game):
        self.game = game
        self.game.eventees.append(self)

        self.selectedObject = None
    
    def select(self, worldObject):
        self.selectedObject = worldObject

    def callEvent(self, event):
        if self.game.gameState == EDIT_STATE:
            if event.key == pg.MOUSEBUTTONDOWN:
                self.place()

    def place():
        print("debug: placing item!")