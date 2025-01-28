from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")
