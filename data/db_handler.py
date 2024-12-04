from tinydb import TinyDB, Query

db = TinyDB('./data/ebenevo.json')
game_db = TinyDB('./data/user_ids.json')
query = Query()