import os
import psycopg2

from api import create_app, db


def create_table():
  # Connects to our database using parameters stored 
  # as environment variables in our system.
  # You can set these in your shell by running:
  # export DB_USER=<your_username>
  # export DB_PASSWORD=<your_password>
  # etc.
  # See set_env.sh for an automatic script to set these
  # easily.
  connection = psycopg2.connect(
      user=os.environ['DB_USER'],
      password=os.environ['DB_PASS'],
      host=os.environ['DB_HOST'],
      database=os.environ['DB_NAME'],
  )

  # Creates a cursor object to execute queries.
  cursor = connection.cursor()

  # Creates a table with the name 'diary_entries'.
  # Our columns will be:
  #   - id: a unique identifier for each entry
  #   - title: the title of the entry
  #   - content: the content of the entry
  #   - datetime: the date and time the entry was posted
  # If a table with the name 'diary_entries' already exists,
  # this will fail.
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS diary_entries
    (
      id serial PRIMARY KEY,
      title VARCHAR(50) NOT NULL,
      content VARCHAR(150) NOT NULL,
      datetime date DEFAULT CURRENT_TIMESTAMP
    )
  """)

  # Commits all changes to the database.
  connection.commit()

  # Closes the connection and the cursor.
  cursor.close()
  connection.close()

if __name__ == '__main__':
  # create_table()
  with app.app_context():
    db.create_all()