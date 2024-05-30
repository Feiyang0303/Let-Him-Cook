import pygame as pg
import math, sys, random

from gameObject import *
from savesystem import *
from player import *
from world import *
from worldEditor import *
from settings import *
from items import Storage

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.world_surf = pg.Surface((WORLD_WIDTH * TILE_WIDTH, WORLD_HEIGHT * TILE_HEIGHT))

        self.FPS = 60
        self.DT = 1/self.FPS
        self.clock = pg.time.Clock()
        self.storage = Storage()

        self.eventees = []

        self.isFreezed = False
        self.isPaused = False
        self.gameState = PLAY_STATE

        self.eventees = []

        self.isFreezed = False
        self.isPaused = False
        self.gameState = PLAY_STATE

        # initialization
    def new_game(self):
        self.world = World(self)
        self.player = Player(self)


    def load_game(self):
        self.world = World(self)
        self.player = Player(self)
        load_game_state(self)

    def set_game_state(self, state):
        self.gameState = state
        self.isFreezed = self.gameState != PLAY_STATE
    
    def check_freeze(self):
        self.isFreezed = self.isPaused or (self.gameState != PLAY_STATE)

    # tickables
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_game_state(self)
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.isPaused = not self.isPaused
                elif event.key == pg.K_i:
                    self.player.show_inventory = not self.player.show_inventory
            
            for eventee in self.eventees:
                eventee.callEvent(event)

    def update(self):
        self.world.update()
        self.player.update()
    
    def immuneUpdate(self):
        self.world.immuneUpdate()
        self.player.immuneUpdate()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOUR)
        self.world.draw()
        self.player.draw()
        if self.player.show_storage:
            self.storage.draw(self.screen)

        self.screen.blit(self.world_surf, (MARGIN, MARGIN))

        pg.display.update()

    def run(self):
        while True:
            self.check_freeze()
            self.events()
            if not self.isFreezed:
                self.update()
            self.immuneUpdate()
            self.draw()
            self.DT = self.clock.tick(self.FPS) / 1000
