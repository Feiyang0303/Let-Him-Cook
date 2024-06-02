import pygame as pg
import math
import sys

from gameObject import *
from settings import *

class WorldEditor(GameObject):
    def __init__(self, game):
        self.game = game
        self.game.eventees.append(self)

        self.selectedBuilding = None
    
    def screen_to_world(pos:pg.Vector2):
        pass

    def place(self, building_id:str):
        self.game.state = EDIT_STATE
        print(f"placing {building_id}!")
    
    def immuneUpdate(self):
        pass
    
    def draw(self):
        pass
        # mouse_pos = self.screen_to_world(pg.mouse.get_pos())
        # pg.draw.rect(self.game.world_surf)
        # self.game.world_surf.blit(highlight, ((pos.x + self.game.world.scroll.x)*TILE_WIDTH + self.spriteRect.x, (pos.y + self.game.world.scroll.y)*TILE_HEIGHT + self.spriteRect.y))