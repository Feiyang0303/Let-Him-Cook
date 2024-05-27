from game import Game
import json


def save_game_state(player):
    game_state = {
      'player position x' : player.x,
      'player position y' : player.y
        
    }

    with open('gamesave.json','w') as f:
     json.dump(game_state,f)

def load_game_state(player):
    try:
      with open('gamesave.json','r') as f:
         game_state = json.load(f)
         return game_state
    
    except FileNotFoundError:
      print("Save File not Found")
      return None