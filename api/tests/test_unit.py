import pytest

from api.models import Blurb
from .utils import current_date

@pytest.mark.freeze_time("2023-03-14 15:09:26")
def test_new_blurb(current_date):
  data = {
    "title": "test note",
    "content": "this is the content of the test note",
    "datetime": current_date
  }

  blurb = Blurb(
    title=data["title"],
    content=data["content"],
    datetime=data["datetime"]
  )

  assert blurb.title == data["title"]
  assert blurb.content == data["content"]
  assert blurb.datetime == data["datetime"]