from tinydb import TinyDB, Query

db = TinyDB('ebenevo.json')
game_db = TinyDB('user_ids.json')
who_game_db = TinyDB('who_game.json')
query = Query()