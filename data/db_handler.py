from tinydb import TinyDB, Query

db = TinyDB('ebenevo.json')
game_db = TinyDB('user_ids.json')
User = Query()