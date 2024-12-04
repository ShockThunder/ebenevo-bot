import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOT_TOKEN')
admin_channel_id = os.getenv('CHANNEL_ID')

whitelist = {
    -1002482107448,
    -1002434589436,
    -1002173225368
}

bebebelist = {
    1491645841,
}