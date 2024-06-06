import pygame as pg
import math
import sys

from settings import *

class GameObject:
    def __init__(self, game, pos:pg.Vector2, hitbox:pg.Vector2, sprite=None, spriteRect:pg.Rect=None) -> None:
        self.game = game

        self.pos = pos
        self.hitbox = hitbox

        if spriteRect == None: self.spriteRect = pg.Rect((0, 0), (self.hitbox.x*TILE_WIDTH, self.hitbox.y*TILE_HEIGHT))
        else: self.spriteRect = spriteRect

        if isinstance(sprite, pg.Surface): self.sprite = sprite
        else: self.sprite = pg.transform.scale(pg.image.load(sprite), self.spriteRect.size)
    
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
