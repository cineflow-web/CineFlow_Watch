from datetime import datetime
from time import time

import pytz

from Backend.helper.database import Database

#----- Shared application state
timezone = pytz.timezone("Asia/Colombo")
now = datetime.now(timezone)
StartTime = time()

USE_DEFAULT_ID: str = None
MANUAL_SESSION: dict = None
db = Database()

__version__ = "1.0.1"
