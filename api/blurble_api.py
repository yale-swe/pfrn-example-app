import os
from types import NoneType
import psycopg2
import typing
import json
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin

from .models import Blurb
from .extensions import db

api = Blueprint("api", __name__)

SELECT_QUERY = """
  SELECT * FROM diary_entries
"""

INSERT_QUERY_START = "INSERT INTO diary_entries (title, content) VALUES (%s, %s);"

"""
  Creates a connection object to our database, which we'll use
  to execute queries.
"""
def get_db_connection():
  connection = psycopg2.connect(
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
  )
  return connection

"""
  Takes a tuple returned by the PostgreSQL database and
  converts it into an object.
"""
def convert_row_to_object(row):
  return {
    'id': row[0],
    'title': row[1],
    'content': row[2],
    'datetime': row[3],
  }

"""
  Gets all entries from our database and returns them 
  back as a JSON string.
"""
@api.route('/')
@cross_origin()
def get_all_entries() -> str:
  results: list[Blurb] = Blurb.query.all()
  res = json.dumps(results, default = str)
  return res

@api.route('/insert', methods=['POST'])
@cross_origin()
def insert_into_db() -> str:
  try:
    data: typing.Dict[str, str] = json.loads(request.data)
    title: str = data['title']
    content: str = data['content']
    datetime: str | NoneType = data['datetime']

    blurb = Blurb(title=title, content=content, datetime=datetime)
    
    db.session.add(blurb)
    db.session.commit()
  
  except Exception as e:
    return 'bad request', 400

  return 'Success'