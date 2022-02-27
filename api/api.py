import os
import psycopg2
import typing
import json
from flask import Flask, request

app = Flask(__name__)

SELECT_QUERY = """
  SELECT * FROM diary_entries
"""

INSERT_QUERY_START = """
  INSERT INTO diary_entries (title, content)
  VALUES (%s, %s)
"""

"""
  Creates a connection object to our database, which we'll use
  to execute queries.
"""
def get_db_connection() -> psycopg2.connection:
  connection = psycopg2.connect(
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
  )
  return connection

"""
  Gets all entries from our database and returns them 
  back as a JSON string.
"""
@app.route('/')
def get_all_entries() -> str:
  # Establish the connection and get the cursor.
  connection: psycopg2.connection = get_db_connection()
  cursor: psycopg2.cursor = connection.cursor()

  # Execute our query.
  cursor.execute(SELECT_QUERY)

  # Fetch the results of the query and store them in
  # a variable. Note that cursor.fetchall() returns 
  # results as a list of tuples.
  # Documentation:
  # https://www.psycopg.org/docs/cursor.html?highlight=fetchall#cursor.fetchall
  results: list[tuple] = cursor.fetchall()

  # Close the cursor and connection.
  cursor.close()
  connection.close()
  return json.dumps(results)

@app.route('/insert', methods=['POST'])
def insert_into_db() -> str:
  # Get the the title and content from the request.
  data: typing.Dict[str, str] = json.loads(request.data)
  title: str = data['title']
  content: str = data['content']

  # Establish the connection and get the cursor.
  connection: psycopg2.connection = get_db_connection()
  cursor: psycopg2.cursor = connection.cursor()

  # Execute our query.
  cursor.execute(INSERT_QUERY_START + f"({title}, {content})")

  # Commit the changes to the database.
  connection.commit()

  # Close the cursor and connection.
  cursor.close()
  connection.close()
  return 'Success'
