from tinydb import TinyDB, Query
from pathlib import Path

curPath = Path(__file__)
dataPath = Path(curPath.parent.parent, 'data')
ebPath = Path(dataPath, 'ebenevo.json')
whoPath = Path(dataPath, 'who_game.json')
print(ebPath)
print(whoPath)
db = TinyDB(ebPath)
who_game_db = TinyDB(whoPath)
query = Query()