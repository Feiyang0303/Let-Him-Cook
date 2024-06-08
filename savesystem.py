import json

import pygame as pg

def save_game_state(game):
    print("saving game...")

    game_state = {
      'playerx' : game.player.pos.x,

      'playery' : game.player.pos.y

      
      # 'building_layer' : game.building_layer

    }

    with open('gamesave.json','w') as f:
      json.dump(game_state,f)

def load_game_state(game):
    try:
      with open('gamesave.json','r') as f:
          game_state = json.load(f)
          game.player.pos = pg.Vector2(game_state["playerx"], game_state["playery"])

          # game.building_layer = game_state["building_layer"]

          return True
    except FileNotFoundError:
      print("Save File not Found")
      return False