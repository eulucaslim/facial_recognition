from dotenv import load_dotenv
from typing import Final
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

FR_HOST : Final[int] = os.getenv("FR_HOST")
FR_PORT : Final[int] = os.getenv("FR_PORT")
