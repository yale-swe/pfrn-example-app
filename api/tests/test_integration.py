import pytest

from .utils import current_date
from api.models import Blurb

# test empty response
def test_get(client):
  res = client.get("/")
  assert b'[]' in res.data

# test post request
@pytest.mark.freeze_time("2023-03-14 15:09:26")
def test_insert(client, app, current_date):
  data = {
    "title": "test note",
    "content": "this is the content of a test note",
    "datetime": current_date
  }

  client.post("/insert", json=data)

  with app.app_context():
    assert Blurb.query.count() == 1

    assert Blurb.query.first().title == data["title"]
    assert Blurb.query.first().content == data["content"]

    assert Blurb.query.first().datetime == data["datetime"]

def test_invalid_insert(client, app, current_date):
  data = {
    "name": "test note",
    "content": "this is the content of a test note",
    "datetime": current_date
  }
  
  res = client.post("/insert", json=data)
  assert res.status_code == 200