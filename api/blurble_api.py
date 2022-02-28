import os
import psycopg2
import typing
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
@app.route('/')
@cross_origin()
def get_all_entries() -> str:
  # Establish the connection and get the cursor.
  connection = get_db_connection()
  cursor: psycopg2.cursor = connection.cursor()

  # Execute our query.
  cursor.execute(SELECT_QUERY)

  # Fetch the results of the query and store them in
  # a variable. Note that cursor.fetchall() returns 
  # results as a list of tuples.
  # Documentation:
  # https://www.psycopg.org/docs/cursor.html?highlight=fetchall#cursor.fetchall
  tuple_results: list[tuple] = cursor.fetchall()

  # Convert each tuple into an object.
  results: list[dict] = list(map(convert_row_to_object, tuple_results))

  # Close the cursor and connection.
  cursor.close()
  connection.close()

  # If we don't know how to serialize a value,
  # automatically seralize it as a string.
  response = json.dumps(results, default=str)
  return response

@app.route('/insert', methods=['POST'])
@cross_origin()
def insert_into_db() -> str:
  # Get the the title and content from the request.
  data: typing.Dict[str, str] = json.loads(request.data)
  title: str = data['title']
  content: str = data['content']

  # Establish the connection and get the cursor.
  connection = get_db_connection()
  cursor: psycopg2.cursor = connection.cursor()

  # Execute our query.
  cursor.execute(INSERT_QUERY_START, (title, content))

  # Commit the changes to the database.
  connection.commit()

  # Close the cursor and connection.
  cursor.close()
  connection.close()
  return 'Success'
