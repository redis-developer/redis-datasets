import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config.update(
    REDIS_HOST=os.getenv('REDIS_HOST') or 'localhost',
    REDIS_PORT=os.getenv('REDIS_PORT') or 6379
)

from app import routes
