import os

from flask import Flask

from .extensions import db
from .blurble_api import api

def create_app(database_uri="postgresql://localhost:5432/{}".format(os.environ["DB_NAME"])):
  app = Flask(__name__)

  app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

  # initialize
  db.init_app(app)

  app.register_blueprint(api)

  return app
