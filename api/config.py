from os import environ, path
from dotenv import load_dotenv

PORT = environ.get('DB_PORT')
HOST = environ.get('DB_HOST')
PASS = environ.get('DB_PASS')
USER = environ.get('DB_USER')

class Config:
  SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}".format(USER, PASS, HOST, PORT)
  