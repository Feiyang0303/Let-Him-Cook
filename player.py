import pygame as pg
import math
import sys

from gameObject import *
from settings import *
from tools import *
from world import *
from items import Storage, Inventory, Item
import random


class PlayerCollisionInfo:
    def __init__(self):
        self.reset()

    def reset(self):
        self.is_colliding = False
        self.collidingX = False
        self.collidingY = False
        self.colliding_right = False
        self.colliding_left = False
        self.colliding_top = False
        self.colliding_down = False
        self.colldiing_tile = None


class Player(GameObject):
    HEAD_OFFSET = pg.Vector2(0, -50)

    def __init__(self, game, control_schema=0):
        self.game = game
        self.pos = pg.Vector2(2, 2)
        self.hitbox = pg.Vector2(PLAYER_HITBOX_HEIGHT, PLAYER_HITBOX_WIDTH)
        self.sprite_rect = pg.Rect(-3*PPU, -19*PPU, 13*PPU, 26*PPU)
        self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-s.png"), self.sprite_rect.size)
        self.game.eventees.append(self)

        self.velocity = pg.Vector2(0, 0)
        self.inventory = Inventory(game, self)

        # Selected Tile
        self.selected_building = None
        self.dir = pg.Vector2(1, 0)

        # Movement Info
        self.collisionInfo = PlayerCollisionInfo()
        self.disable_movement_cap_timer = 0

        self.controls = {}
        if control_schema == 0:
            self.controls["up"] = pg.K_w
            self.controls["down"] = pg.K_s
            self.controls["right"] = pg.K_d
            self.controls["left"] = pg.K_a
            self.controls["dash"] = pg.K_LSHIFT
            self.controls["interact"] = pg.K_e
        else:
            self.controls["up"] = pg.K_UP
            self.controls["down"] = pg.K_DOWN
            self.controls["right"] = pg.K_RIGHT
            self.controls["left"] = pg.K_LEFT
            self.controls["dash"] = pg.K_KP_0
            self.controls["interact"] = pg.K_RSHIFT

    def update(self):
        self.move()

    def call_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.controls["interact"]:
                if self.selected_building != None:
                    self.selected_building.interact(self)
                    if isinstance(self.selected_building, Fridge):
                        if self.game.state != FRIDGE_STATE:
                            self.game.state = FRIDGE_STATE
            elif event.key == self.controls["dash"]:
                self.velocity = self.dir * DASH_POWER
                self.disable_movement_cap_timer = TIME_TO_TAKE_DASH
            elif event.key == pg.K_i:
                self.inventory.toggle_inventory()
            elif event.key == pg.K_SPACE:
                item = random.choice(["sugar", "butter", "flour"])
                self.inventory.add_item(item)

    def set_sprite(self):
        if self.dir.y == 1 and self.dir.x == 1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-se.png"), self.sprite_rect.size)
        elif self.dir.y == 1 and self.dir.x == -1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-sw.png"), self.sprite_rect.size)
        elif self.dir.y == 1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-s.png"), self.sprite_rect.size)
        elif self.dir.x == 1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-e.png"), self.sprite_rect.size)
        elif self.dir.x == -1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-w.png"), self.sprite_rect.size)
        
        if self.dir.y == -1:
            self.sprite = pg.transform.scale(pg.image.load("new-sprites/player/player-n.png"), self.sprite_rect.size)

    def move(self):
        keys = pg.key.get_pressed()

        orth = pg.Vector2(0, 0)
        if keys[self.controls["right"]]:
            self.dir.x = 1
            orth.x = 1
            if self.velocity.x < 0: self.velocity.x = 0
        if keys[self.controls["left"]]:
            self.dir.x = -1
            orth.x = -1
            if self.velocity.x > 0: self.velocity.x = 0
        if keys[self.controls["up"]]:
            self.dir.y = -1
            orth.y = -1
            if self.velocity.y > 0: self.velocity.y = 0
        if keys[self.controls["down"]]:
            self.dir.x = 1
            orth.y = 1
            if self.velocity.y < 0: self.velocity.y = 0
        if keys[self.controls["up"]] or keys[self.controls["down"]] or keys[self.controls["left"]] or keys[self.controls["right"]]:
            self.dir = orth.copy()

        acceleration = (1 if (orth[0] == 0 or orth[1] == 0) else 0.7071) * orth * PLAYER_ACCELERATION

        if self.disable_movement_cap_timer <= 0:
            if not (keys[self.controls["right"]] or keys[self.controls["left"]]):
                acceleration.x = -sign(self.velocity.x) * min(abs(self.velocity.x / self.game.DT), PLAYER_DECELERATION)
            if not (keys[self.controls["up"]] or keys[self.controls["down"]]):
                acceleration.y = -sign(self.velocity.y) * min(abs(self.velocity.y / self.game.DT), PLAYER_DECELERATION)

            self.velocity += acceleration * self.game.DT

        max_speed = (1 if (orth[0] == 0 or orth[1] == 0) else 0.7071) * PLAYER_MAX_SPEED
        if self.disable_movement_cap_timer > 0:
            max_speed = math.inf
            self.disable_movement_cap_timer -= self.game.DT
        self.velocity = pg.Vector2(clampAbsolute(self.velocity.x, max_speed), clampAbsolute(self.velocity.y, max_speed))

        self.try_move(self.velocity * self.game.DT)
        self.get_selected_tile()

    def try_move(self, delta: pg.Vector2):
        self.collisionInfo.reset()

        # resolve x collisions first before the other
        fposx = pg.Vector2(self.pos.x + delta.x, self.pos.y)

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                tile = self.game.world.get(x, y)

                isSolidBuilding = isinstance(tile, Building) and tile.isSolid
                if not isSolidBuilding: continue

                if (are_hitboxes_colliding(fposx, self.hitbox, tile.pos, tile.hitbox)):
                    self.collisionInfo.is_colliding = True
                    self.collisionInfo.collidingX = True
                    self.collisionInfo.colliding_left = delta.x < 0
                    self.collisionInfo.colliding_right = delta.x > 0

                    if self.collisionInfo.colliding_right:
                        self.pos.x = tile.pos.x - self.hitbox.x
                    else:
                        self.pos.x = tile.pos.x + tile.hitbox.x

        if not self.collisionInfo.collidingX:
            self.pos.x += delta.x

        # now we can safely do y collisions! hoorah

        fposy = pg.Vector2(self.pos.x, self.pos.y + delta.y)

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                tile = self.game.world.get(x, y)

                isSolidBuilding = isinstance(tile, Building) and tile.isSolid
                if not isSolidBuilding: continue

                if (are_hitboxes_colliding(fposy, self.hitbox, tile.pos, tile.hitbox)):
                    self.collisionInfo.is_colliding = True
                    self.collisionInfo.collidingY = True
                    self.collisionInfo.colliding_top = delta.y < 0
                    self.collisionInfo.colliding_down = delta.y > 0

                    if self.collisionInfo.colliding_top:
                        self.pos.y = tile.pos.y + tile.hitbox.y
                    else:
                        self.pos.y = tile.pos.y - self.hitbox.y

        if not self.collisionInfo.collidingY:
            self.pos.y += delta.y

        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0

        if self.pos.x > WORLD_WIDTH - self.hitbox.x:
            self.pos.x = WORLD_WIDTH - self.hitbox.x
        if self.pos.y > WORLD_HEIGHT - self.hitbox.y:
            self.pos.y = WORLD_HEIGHT - self.hitbox.y

    def get_selected_tile(self):
        rounded_pos = pg.Vector2(int(self.pos.x + PLAYER_HITBOX_WIDTH/2), int(self.pos.y + PLAYER_HITBOX_HEIGHT/2))
        selected_pos = rounded_pos + self.dir
        self.selected_building = self.game.world.get(int(selected_pos.x), int(selected_pos.y))
        if not isinstance(self.selected_building, Building):
            self.selected_building = None

    def draw(self):
        self.set_sprite()
        self.game.world_renderer.draw_object(self)

        if self.selected_building != None:
            self.selected_building.draw_highlighted()

        self.inventory.draw()



