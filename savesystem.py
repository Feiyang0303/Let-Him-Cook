import json

import pygame as pg

def save_game_state(game):
    print("saving game...")

    building_storage = []
    for building_row in game.world.building_layer:
      id_row = []
      for building in building_row:
        id_row.append(building.id)
      building_storage.append(id_row)
    print("\n".join([str(row) for row in building_storage]))


    game_state = {
      'playerx' : game.player.pos.x,
      'playery' : game.player.pos.y,
      'building_layer' : building_storage,
      'money' : game.money
      }

    with open('gamesave.json','w') as f:
      json.dump(game_state,f)

def load_game_state(game):
    try:
      with open('gamesave.json','r') as f:
          game_state = json.load(f)
          building_storage = game_state["building_layer"]
          # building_storage = game_state["building_layer"]
          game.player.pos = pg.Vector2(game_state["playerx"], game_state["playery"])
      
          for y, building_row in enumerate(building_storage):
            for x, buildingid in enumerate(building_row):
              if buildingid != "empty":
                game.world.place(buildingid, pg.Vector2(x, y))
          game.money = game_state["money"]

      return True
    except:
      print("Save File not Found, resetting save...")
      return False