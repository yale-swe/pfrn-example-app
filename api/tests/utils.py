import pytest
import datetime

@pytest.fixture()
def current_date():
  return datetime.datetime.utcnow()