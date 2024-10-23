import os

from settings import project_path
from src.sql.bd import BotDB

BotDB = BotDB(f"{project_path}{os.sep}db.db")

