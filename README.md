# Yale SWE PFRN Example App (Incomplete)

The PFRN stack consists of the following popular frameworks:
  - [PostgreSQL](https://www.postgresql.org/), a popular relational database
  - [Flask](https://flask.palletsprojects.com/en/2.0.x/), a popular web framework 
  - [React Native](https://reactnative.dev/), a popular mobile framework

**This repository is most helpful for those comfortable with with relational
databases and Python.** Knowledge of Javascript and React Native is also helpful for front-end development, but not
a requirement.

This tutorial will not only go over the basics of how to use these frameworks, 
but also how to set up your environment.

We'll be be creating a simple diary app where users can write a quick blurbs about how they're feeling at that moment, and then look back at all the notes they've written in the past. 

## Step 0: Install PostgreSQL, Flask, and React Native

**NOTE**: ***Dependencies are tricky!*** In a stack which utilizes multiple languages and frameworks, it could be difficult to keep track of everything. This is one of the drawbacks of using a mixed stack like this, but once you get grasp on the core concepts, building upon them is easy.

This section will walk you through installing the dependencies for this tutorial. It may be helpful to consider using [Docker containers](https://www.docker.com/) to create a consistent and clean environment where you can install these dependencies and provide a consistent system state across your team. This is something to explore outside of this tutorial.

### Using virtual environments for Python dependencies
The cleanest way to install Python dependencies for a project is to use virtual environments. This allows you to contain all packages within an isolated Python environment, which you can turn off and on as needed. 

There are multiple virtual environment packages you can add to your primary Python installation, but for this tutorial we will use `venv`, which comes automatically with the Python programming language. 

You can create a virtual environment in your current directory by running
```bash
python3 -m venv <YOUR_ENVIORNMENT_NAME>
source <YOUR_ENVIRONMENT_NAME>/bin/activate # For Unix or MacOS
```

If you have a Windows machine, or want to learn more, consult the [venv documentation](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) for more information.

### Installing Flask

You can install Flask through Python's [pip](https://pip.pypa.io/en/stable/) package manager:
```bash
pip install Flask
```

### Installing Postgres

You can install Postgres for your operating system by following the instructions on the [Postgres website](https://www.postgresql.org/download/). For MacOS uses, the recommneded way is to do so using [Homebrew](https://brew.sh/). Once installed, the command is simply:
```bash
brew install postgresql
```

### Installing React Native

**NOTE:** Installing React Native also requires [Node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com/). If you don't have these installed, follow [this guide](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm). 

Once you have Node.js and npm installed, we can utilize the Expo CLI to install React Native and build/test our app quickly. The command to do so is:
```bash
npm install -g expo-cli
```

To learn more, check out the [React Native environment setup guide](https://reactnative.dev/docs/environment-setup)

## Step 1: Setting up your project

Now that your dependencies are installed, it's time to start setting up your project and writing some prelimiary code! 
We'll start from the bottom up, first building our database, then creating our Flask API, and finally creating our React Native app.

### Building your database

There are a variety of different ways to build your Postgres database, but one of the most straightforward ways is to log in to a Postgres session as an administrator and manage your work from there. We'll do so using the `psql` command. `psql` is a command line utility that allows you to interact with a Postgres database.

You can login to Postgres the as default administator `postgres` by running:

```bash
pg_ctl -D /usr/local/var/postgres -l logfile start # Starts the postgresql server
brew services start postgresql # Alternatively, if installed through Homebrew.
```

```bash
psql postgres
```

This will open up the Postgres command line interface. You can use this to create a new database, or to manage your existing databases. We'll create a database named `pfrn_db` (but you can use whichever name you want), create a user for our database, and grant the user administrative privileges to the database:
```
postgres=# CREATE DATABASE pfrn_db; 
postgres=# CREATE USER pfrn_user WITH PASSWORD 'pfrn_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE pfrn_db TO pfrn_user;
```

The password can be whatever you want. Note that the semicolon is necessary at the end of each command.

We can confirm that our database was create by running:
```
postgres=# \l
```

You should see `pfrn_db` listed as one of your databases. Once confirmed, exit the session by running:
```
postgres=# \q
```

### Creating your Flask API and linking to your database

Now that we have our database set up, we can create our Flask API and connect the two! 

#### Creating a new table in our database via Python

First, we need to install the [pyscopg2](https://www.psycopg.org/) package. This is a Python package that allows us to connect to Postgres. Install it using `pip` via the command:
```bash
pip install psycopg2-binary
```

Now we need to to write the code to connect and interact with our database. In this tutorial, we'll create a table named `diary_entries` with rows `id`, `title`, `blurb`, and `date_posted`. See `api/create_table.py` to see how to do this. 

Once you understand the code, run `python api/create_table.py` to create the table.

Note how you can create a table both programatically, and with the `psql` CLI. For your project, determine what's best, and implement your solution accordingly. 


#### Creating a Flask API to read and write to our new table

Now that we have our table, let's create the API that will handle read and write operations. 

We'll create two routes for our API:
 - `/`:  This will return all entries in the table.
 - `/insert`: This will insert a new entry into the table.

In the `api/api.py` file, you will see how Flask handles these routes, and how we gather information from the 
database with these routes. 

TODO: Continue from here.

### NOTES

Make sure to stop your Postgres session when you're done by running:
```bash
pg_ctl -D /usr/local/var/postgres -l logfile stop # Stops the postgresql server
brew services stop postgresql # Alternatively, if installed through Homebrew.
```
You can also install python dependencies from requirements.txt



