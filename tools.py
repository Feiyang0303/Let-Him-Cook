import pygame as pg
from gameObject import GameObject

def is_point_in_hitbox(point, pos, hitbox):
    return (point.x >= pos.x and point.x <= pos.x + hitbox.x) and \
            (point.y >= pos.y and point.y <= pos.y + hitbox.y)

def are_hitboxes_colliding(pos1, hitbox1, pos2, hitbox2):
    return not (pos1.y >= pos2.y + hitbox2.y or pos1.y + hitbox1.y <= pos2.y or
                pos1.x >= pos2.x + hitbox2.x or pos1.x + hitbox1.x <= pos2.x)

def clampAbsolute(x, bound):
    return max(-bound, min(x, bound))

def sign(x):
    if x < 0: return -1
    elif x > 0: return 1
    else: return 0

# def are_hitboxes_colliding(go1, go2):
#     return not (go1.pos.y >= go2.pos.y + go2.hitbox.y or go1.pos.y + go1.hitbox.y <= go2.pos.y or
#                 go1.pos.x >= go2.pos.x + go2.hitbox.x or go1.pos.x + go1.hitbox.x <= go2.pos.x)