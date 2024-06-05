import pygame as pg
import math
import sys

from gameObject import *
from settings import *
from tools import *
from world import *
from items import Storage, Inventory, Item

class PlayerCollisionInfo:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.isColliding = False
        self.collidingX = False
        self.collidingY = False
        self.collidingRight = False
        self.collidingLeft = False
        self.collidingTop = False
        self.collidingDown = False
        self.collidingTile = None


class Player(GameObject):
    HEAD_OFFSET = pg.Vector2(0, -50)
    def __init__(self, game):
        self.game = game
        self.pos = pg.Vector2(2, 2)
        self.hitbox = pg.Vector2(PLAYER_HITBOX_HEIGHT, PLAYER_HITBOX_WIDTH)
        self.spriteRect = pg.Rect(0, 0, TILE_WIDTH*PLAYER_HITBOX_HEIGHT, TILE_HEIGHT*PLAYER_HITBOX_HEIGHT)
        self.sprite = pg.transform.scale(pg.image.load("sprites/Cookie.png"), self.spriteRect.size)

        self.velocity = pg.Vector2(0, 0)

        self.game.eventees.append(self)
        
        # Selected Tile
        self.selected_building = None
        self.dir = pg.Vector2(1, 0)

        # Collision Info
        self.collisionInfo = PlayerCollisionInfo()

        self.disable_movement_cap_timer = 0
        self.inventory = Inventory()

    def update(self):
        self.move()
    
    def callEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                if self.selected_building != None:
                    self.selected_building.interact()
            elif event.key == pg.K_LSHIFT:
                self.velocity = self.dir * DASH_POWER
                self.disable_movement_cap_timer = TIME_TO_TAKE_DASH
            elif event.key == pg.K_i:
                self.inventory.toggle_inventory()
                print("inventory shows")
            elif event.key == pg.K_SPACE:
                item=Item('Sugar', 'sprites/Sugar.png')
                self.inventory.push(item)
                print("item added to inventory")

    def move(self):
        keys = pg.key.get_pressed()

        orth = pg.Vector2(0, 0)
        if keys[pg.K_d]:
            self.dir.x = 1
            orth.x = 1
            if self.velocity.x < 0: self.velocity.x = 0
        if keys[pg.K_a]:
            self.dir.x = -1
            orth.x = -1
            if self.velocity.x > 0: self.velocity.x = 0
        if keys[pg.K_w]:
            self.dir.y = -1
            orth.y = -1
            if self.velocity.y > 0: self.velocity.y = 0
        if keys[pg.K_s]:
            self.dir.x = 1
            orth.y = 1
            if self.velocity.y < 0: self.velocity.y = 0
        if keys[pg.K_d] or keys[pg.K_a] or keys[pg.K_w] or keys[pg.K_s]:
            self.dir = orth.copy()
        
        acceleration = (1 if (orth[0]==0 or orth[1]==0) else 0.7071) * orth * PLAYER_ACCELERATION

        if self.disable_movement_cap_timer <= 0:
            if not (keys[pg.K_d] or keys[pg.K_a]):
                acceleration.x = -sign(self.velocity.x) * min(abs(self.velocity.x / self.game.DT), PLAYER_DECELERATION)
            if not (keys[pg.K_w] or keys[pg.K_s]):
                acceleration.y = -sign(self.velocity.y) * min(abs(self.velocity.y / self.game.DT), PLAYER_DECELERATION)

            self.velocity += acceleration * self.game.DT
        
        max_speed = (1 if (orth[0]==0 or orth[1]==0) else 0.7071) * PLAYER_MAX_SPEED
        if self.disable_movement_cap_timer > 0:
            max_speed = math.inf
            self.disable_movement_cap_timer -= self.game.DT
        self.velocity = pg.Vector2(clampAbsolute(self.velocity.x, max_speed), clampAbsolute(self.velocity.y, max_speed))

        self.try_move(self.velocity * self.game.DT)
        self.get_selected_tile()

    def try_move(self, delta:pg.Vector2):
        self.collisionInfo.reset()

        # resolve x collisions first before the other
        fposx = pg.Vector2(self.pos.x + delta.x, self.pos.y)

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                tile = self.game.world.get(x, y)

                isSolidBuilding = isinstance(tile, Building) and tile.isSolid
                if not isSolidBuilding: continue

                if (are_hitboxes_colliding(fposx, self.hitbox, tile.pos, tile.hitbox)):
                    self.collisionInfo.isColliding = True
                    self.collisionInfo.collidingX = True
                    self.collisionInfo.collidingLeft = delta.x < 0
                    self.collisionInfo.collidingRight = delta.x > 0

                    if self.collisionInfo.collidingRight:
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
                    self.collisionInfo.isColliding = True
                    self.collisionInfo.collidingY = True
                    self.collisionInfo.collidingTop = delta.y < 0
                    self.collisionInfo.collidingDown = delta.y > 0

                    if self.collisionInfo.collidingTop:
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
        rounded_pos = pg.Vector2(round(self.pos.x), round(self.pos.y))
        selected_pos = rounded_pos + self.dir
        self.selected_building = self.game.world.get(int(selected_pos.x), int(selected_pos.y))
        if not isinstance(self.selected_building, Building):
            self.selected_building = None

    def draw(self):
        self.game.world_renderer.draw_object(self)

        if self.selected_building != None:
            self.selected_building.draw_highlighted()

        if self.inventory.show_inventory:
            print("draw inventory")
            self.inventory.draw(self.game.screen, self.pos.x, self.pos.y)

    

