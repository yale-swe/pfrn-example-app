import pytest

from api import create_app, db

@pytest.fixture()
def app():
  app = create_app()

  # setup
  with app.app_context():
    db.create_all()

  yield app

  # teardown
  with app.app_context():
    db.drop_all()

@pytest.fixture()
def client(app):
  return app.test_client()

