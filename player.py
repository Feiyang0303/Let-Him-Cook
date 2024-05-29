import pygame as pg
import math
import sys

from gameObject import *
from settings import *

class Player(GameObject):
    def __init__(self, game):
        self.game = game
        self.game.eventees.append(self)
        self.show_storage = False
        self.x, self.y = 2, 2
        self.mspeed = PLAYER_MOVEMENT_SPEED    

    def update(self):
        self.move()

    def move(self):
        keys = pg.key.get_pressed()

        orth = [0, 0]
        if keys[pg.K_d]:
            orth[0] = 1
        if keys[pg.K_a]:
            orth[0] = -1
        if keys[pg.K_w]:
            orth[1] = 1
        if keys[pg.K_s]:
            orth[1] = -1
        
        mult = self.mspeed * (1 if (orth[0]==0 or orth[1]==0) else 0.7071)

        self.try_move(orth[0] * mult, orth[1] * mult)

    def try_move(self, dx, dy):
        self.x += dx * self.game.DT
        self.y += dy * self.game.DT

    def serialize_state(self):
        return {
            'x': self.x,
            'y': self.y
        }

    def draw(self):
        pg.draw.rect(self.game.screen, (255, 255, 255),
                     (self.x * TILE_WIDTH, SCREEN_HEIGHT - self.y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

    def toggle_storage(self):
        self.show_storage = not self.show_storage
