from tinydb import TinyDB, Query

db = TinyDB('./data/ebenevo.json')
game_db = TinyDB('./data/user_ids.json')
who_game_db = TinyDB('./data/who_game.json')
query = Query()