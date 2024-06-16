import pygame as pg
import math
import sys

from gameObject import *
from settings import *
from world import *

class WorldEditor(GameObject):
    def __init__(self, game):
        self.game = game
        self.game.eventees.append(self)

        self.held_building = None
        self.selected_building = None
    
    def call_event(self, event):
        if self.game.state == EDIT_STATE:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.game.world.is_legible_tile_placement(self.held_building.id, self.held_building.pos):
                    self.game.world.place(self.held_building.id, self.held_building.pos)
                    self.game.set_game_state(PLAY_STATE)
        elif self.game.state == DELETE_STATE:
            # i forsee bad things with this event chaining... maybe some sort of status design pattern would be good
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.selected_building != None and not type(self.selected_building) is EmptyTile:
                    self.game.world.destroy(self.selected_building.pos)
                self.game.set_game_state(PLAY_STATE)
        elif self.game.state == MOVE_STATE:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.selected_building != None and not type(self.selected_building) is EmptyTile:
                    self.game.world.destroy(self.selected_building.pos)
                    self.place(self.selected_building.id)

    def place(self, id:str):
        self.game.set_game_state(EDIT_STATE)

        world_pos = self.game.world_renderer.worldspace_pos(pg.Vector2(pg.mouse.get_pos()))
        rounded_pos = pg.Vector2(round(world_pos.x), round(world_pos.y))

        self.held_building = self.game.tile_library[id].copy(rounded_pos)
    
    def immune_update(self):
        world_pos = self.game.world_renderer.worldspace_pos(pg.Vector2(pg.mouse.get_pos()))
        rounded_pos = pg.Vector2(int(world_pos.x), int(world_pos.y))

        if self.game.state == EDIT_STATE:
            self.held_building.pos = rounded_pos
        elif self.game.state == DELETE_STATE or self.game.state == MOVE_STATE:
            self.selected_building = self.game.world.get(rounded_pos.x, rounded_pos.y)
        
    def draw(self):
        if self.game.state == EDIT_STATE:
            self.held_building.draw_ghost()
        elif self.game.state == DELETE_STATE:
            if self.selected_building != None and not type(self.selected_building) is EmptyTile:
                self.selected_building.draw_red(layer=1)
        elif self.game.state == MOVE_STATE:
            if self.selected_building != None and not type(self.selected_building) is EmptyTile:
                self.selected_building.draw_blue(layer=1)