from dotenv import load_dotenv
from typing import Final
import os

load_dotenv()

FR_HOST : Final[int] = os.getenv("FR_HOST")
FR_PORT : Final[int] = os.getenv("FR_PORT")
