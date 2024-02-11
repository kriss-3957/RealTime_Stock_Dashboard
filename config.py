#Config.py file

import os 
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
ALPACA_API_KEY = os.getenv('APCA_API_KEY_ID')
APCA_API_BASE_URL='https://paper-api.alpaca.markets'
            

