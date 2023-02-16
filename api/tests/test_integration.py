import pytest

from api.models import Blurb
from .utils import current_date

# test empty response
def test_get(client):
  res = client.get("/")
  assert b'[]' in res.data

# test post request
@pytest.mark.freeze_time("2023-03-14 15:09:26")
def test_insert(client, app, current_date):
  
  data = {
    "title": "test note", 
    "content": "this is the content of the test note",
    "datetime": current_date
  }

  client.post("/insert", json=data)

  with app.app_context():
    assert Blurb.query.count() == 1

    # check the first and only query
    assert Blurb.query.first().title == data["title"]
    assert Blurb.query.first().content == data["content"]

    # check day time freezed with pytest freeze gun
    assert Blurb.query.first().datetime == current_date