
import pygame as pg

from settings import *

class DrawCall:
    def __init__(self, sprite:pg.Surface, pos:pg.Vector2, spriteRect:pg.Rect, alpha:int=255) -> None:
        self.sprite = sprite
        self.pos = pos
        self.spriteRect = spriteRect
        self.alpha = alpha

class WorldRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.draw_call = []
        self.img = pg.Surface((WORLD_WIDTH * TILE_WIDTH, (WORLD_HEIGHT + WORLD_WALL_HEIGHT) * TILE_HEIGHT))
        self.scroll = pg.Vector2(0, WORLD_WALL_HEIGHT)

    def draw_object_immediate(self, go, sprite=None):
        screenspace_pos = ((go.pos.x + self.scroll.x)*TILE_WIDTH + go.spriteRect.x, (go.pos.y + self.scroll.y)*TILE_HEIGHT + go.spriteRect.y)
        if sprite == None:
            self.img.blit(go.sprite, screenspace_pos)
        else:
            self.img.blit(sprite, screenspace_pos)

    def draw_object(self, go, sprite=None, pos=None, alpha=255):
        sprite = go.sprite if sprite==None else sprite
        pos = go.pos if pos==None else pos

        self.draw_call.append(DrawCall(sprite, pos, go.spriteRect, alpha))
    
    def draw(self):
        # self.img.fill((255, 255, 255))

        self.draw_call.sort(key=lambda dc: dc.pos.y)
        for dc in self.draw_call:
            screenspace_pos = ((dc.pos.x + self.scroll.x)*TILE_WIDTH + dc.spriteRect.x, (dc.pos.y + self.scroll.y)*TILE_HEIGHT + dc.spriteRect.y)

            if (dc.sprite == None): continue
            # dc.sprite = dc.sprite.convert_alpha()
            # dc.sprite.fill((255, 255, 255, 128), None, pg.BLEND_RGBA_MULT)
            print(type(dc))
            dc.sprite.set_alpha(dc.alpha)

            self.img.blit(dc.sprite, screenspace_pos)
            # self.img.blit(dc.sprite, screenspace_pos)
        
        self.game.screen.blit(self.img, (MARGIN, MARGIN + STATS_MARGIN))

        self.draw_call.clear()
