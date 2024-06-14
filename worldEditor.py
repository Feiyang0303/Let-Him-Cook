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

    def place(self, id:str):
        self.game.set_game_state(EDIT_STATE)

        world_pos = self.game.world_renderer.worldspace_pos(pg.Vector2(pg.mouse.get_pos()))
        rounded_pos = pg.Vector2(round(world_pos.x), round(world_pos.y))

        self.selectedBuilding = self.game.tile_library[id].copy(rounded_pos)
    
    def immuneUpdate(self):
        if self.game.state == EDIT_STATE:
            world_pos = self.game.world_renderer.worldspace_pos(pg.Vector2(pg.mouse.get_pos()))
            rounded_pos = pg.Vector2(int(world_pos.x), int(world_pos.y))

            self.selectedBuilding.pos = rounded_pos
    
    def call_event(self, event):
        if self.game.state == EDIT_STATE:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.game.world.is_legible_tile_placement(self.selectedBuilding.id, self.selectedBuilding.pos):
                    self.game.world.place(self.selectedBuilding.id, self.selectedBuilding.pos)
                    self.game.set_game_state(PLAY_STATE)
        
    def draw(self):
        if self.game.state == EDIT_STATE:
            self.selectedBuilding.draw_ghost()