import os
from enum import Enum

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
PORT = int(os.getenv('PORT', 9090))
DATA_DIR = 'input_data'
MOCK_DATA_FILENAME = 'mock_posts.csv'
STATS_TABLE = 'posts_metrics'

POSTGRES_CONNECTION_STRING = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

