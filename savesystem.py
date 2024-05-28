import json

def save_game_state(game):
    print("saving game...")

    game_state = {
      'playerx' : game.player.x,
      'playery' : game.player.y
    }

    with open('gamesave.json','w') as f:
      json.dump(game_state,f)

def load_game_state(game):
    try:
      with open('gamesave.json','r') as f:
          game_state = json.load(f)
          game.player.x, game.player.y = game_state["playerx"], game_state["playery"]
          return True
    except FileNotFoundError:
      print("Save File not Found")
      return False