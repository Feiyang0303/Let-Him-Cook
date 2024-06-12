
import pygame as pg
from gameObject import *

class Particle(GameObject):
    def __init__(self, game, pos: pg.Vector2, hitbox: pg.Vector2, sprite=None, spriteRect: pg.Rect = None) -> None:
        super().__init__(game, pos, hitbox, sprite, spriteRect)
    