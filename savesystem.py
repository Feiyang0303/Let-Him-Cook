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
      'building_layer' : building_storage
          
      }

    with open('gamesave.json','w') as f:
      json.dump(game_state,f)

def load_game_state(game):
    try:
      with open('gamesave.json','r') as f:
          game_state = json.load(f)
          # building_storage = game_state["building_layer"]
          game.player.pos = pg.Vector2(game_state["playerx"], game_state["playery"])

          # for building_tile in building_storage:
          #    if building_tile != "empty":
          #       building_storage[building_tile] = building_storage
          # for row in building_storage:
          #     for i, building_tile in enumerate(row):
          #         if building_tile == "empty":
          #             row[i] = building_storage
                
                
          

          return True
    except FileNotFoundError:
      print("Save File not Found")
      return False