
import pygame as pg

from settings import *

class DrawCall:
    def __init__(self, sprite:pg.Surface, pos:pg.Vector2, offset:pg.Vector2=pg.Vector2(0, 0), z=0, layer=0) -> None:
        self.sprite = sprite
        self.pos = pos
        self.offset = offset
        self.z = z
        self.layer = layer

class WorldRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.draw_call = []
        self.img = pg.Surface((WORLD_WIDTH * TILE_WIDTH, (WORLD_HEIGHT + WORLD_WALL_HEIGHT) * TILE_HEIGHT))
        self.scroll = pg.Vector2(0, WORLD_WALL_HEIGHT)

        self.wall_image = pg.transform.scale(pg.image.load("new-sprites/buildings/wall.png"), (TILE_WIDTH, TILE_HEIGHT))

    def worldspace_pos(self, screen_pos):
        x = (screen_pos.x - MARGIN) / TILE_WIDTH - self.scroll.x
        y = (screen_pos.y - MARGIN - STATS_MARGIN) / TILE_HEIGHT - self.scroll.y
        return pg.Vector2(x, y)

    def draw_object_immediate(self, go, sprite=None):
        screenspace_pos = ((go.pos.x + self.scroll.x)*TILE_WIDTH + go.sprite_rect.x, (go.pos.y + self.scroll.y)*TILE_HEIGHT + go.sprite_rect.y)
        if sprite == None:
            self.img.blit(go.sprite, screenspace_pos)
        else:
            self.img.blit(sprite, screenspace_pos)

    def draw_object(self, go, sprite:pg.Surface=None, pos:pg.Vector2=None, offset:pg.Vector2=None, z=0, layer=0):
        sprite = go.sprite if sprite==None else sprite
        pos = go.pos if pos==None else pos
        offset = pg.Vector2(go.sprite_rect.x, go.sprite_rect.y) if offset==None else offset

        self.draw_call.append(DrawCall(sprite, pos, offset, z, layer))

    
    def draw(self):
        [[self.img.blit(self.wall_image, (x*TILE_WIDTH, y*TILE_HEIGHT)) for x in range(WORLD_WIDTH)] for y in range(WORLD_WALL_HEIGHT)]

        self.draw_call.sort(key=lambda dc: dc.pos.y + dc.layer / 10)
        for dc in self.draw_call:
            screenspace_pos = ((dc.pos.x + self.scroll.x)*TILE_WIDTH + dc.offset.x, (dc.pos.y + self.scroll.y - dc.z)*TILE_HEIGHT + dc.offset.y)
            self.img.blit(dc.sprite, screenspace_pos)
        
        self.game.screen.blit(self.img, (MARGIN, MARGIN + STATS_MARGIN))

        self.draw_call.clear()

