import json

import pygame as pg

def save_game_state(game):
    print("saving game...")

    game_state = {
      'playerx' : game.player.pos.x,
<<<<<<< Updated upstream
      'playery' : game.player.pos.y
=======
<<<<<<< HEAD
      'playery' : game.player.pos.y,
      # 'building_layer' : game.building_layer
=======
      'playery' : game.player.pos.y
>>>>>>> c9ec5341b8278ad75f9c918f45b358f492822f3d
>>>>>>> Stashed changes
    }

    with open('gamesave.json','w') as f:
      json.dump(game_state,f)

def load_game_state(game):
    try:
      with open('gamesave.json','r') as f:
          game_state = json.load(f)
          game.player.pos = pg.Vector2(game_state["playerx"], game_state["playery"])
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
          # game.building_layer = game_state["building_layer"]
=======
>>>>>>> c9ec5341b8278ad75f9c918f45b358f492822f3d
>>>>>>> Stashed changes
          return True
    except FileNotFoundError:
      print("Save File not Found")
      return False