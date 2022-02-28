# Yale SWE PFRN Example App

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
pip install flask-cors # To allow cross-origin requests
```

**NOTE:** that your pip version may be outdated in your enviroment. If you see error messages when trying to install or run packages in your virtual environment, you may need to update your pip version. Yuo can do so using the following command:
```bash
pip install --upgrade pip
```
while in your environment.

### Installing PostgreSQL

You can install Postgres for your operating system by following the instructions on the [Postgres website](https://www.postgresql.org/download/). For MacOS uses, the recommneded way is to do so using [Homebrew](https://brew.sh/). Once installed, the command is simply:
```bash
brew install postgresql
```

#### If you run into import errors later on...
For MacOS, you will also need to install `libpq`, which is the C API for PostgreSQL. You can install this using `brew install libpq`. You'll also need to link the library with `brew link libpq --force`. If any other targets are linked, you'll need to unlink them before re-linking. with `brew unlink postgresql`. 

After you're done with that, you'll need to add the path `export PATH="/usr/local/opt/libpq/bin:$PATH"` to your `.zshrc` or `.bash_profile`. 

Examples like this are why it's beneficial to use a consistent Docker environment to run projects. 

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

In the `api/bundle_api.py` file, you will see how Flask handles these routes, and how we gather information from the 
database with these routes. Refer to this file and make sure that you understand the code.

Before we can run our API, we'll need to set some environment variables so that Flask knows where and how to run the server. These two variables can be set as such:
```bash
export FLASK_APP=blurble_api
export FLASK_ENV=development
```

and then we can start our server with (make sure you're in the `api` directory):
```bash
flask run
```
#### Testing the API and database are linked successfully

Now we will test that our API successfully reads and writes to our database. Make sure that both your postgres database and your Flask API are running.

Next, we'll use a REST client to make some requests to our API. There are a variety of options for REST clients, a nice and lightweight option is the [Advanced Rest Client](https://install.advancedrestclient.com/install). 

Using our client, send a `GET` request to `http://localhost:5000/` to get all entries in the table. You should get a `200 OK` response code, and an empty list. Now make a `POST` request to `http://localhost:5000/insert` with the following JSON body:
```json
{
    "title": "My first entry",
    "blurb": "This is my first entry",
}
```
You can change the title and blurb to whatever you want. Note that the `id` and `datetime` fields will be automatically generated by the database. You should get a `200 OK` response code, and a response string saying `Success`. 

Now, send another `GET` request to `http://localhost:5000/` to get all entries in the table. You should get a `200 OK` response code, and a see a JSON string returned with your title and blurb.

If this works, it means your API and database are linked successfully! The backend of your the app is working. Next, we'll go over what it takes to get started working with a React Native app, and then we'll link your frontend (React Native App) and backend (Flask API that gets info from PostgreSQL database) together.

### Creating our React Native app

Create your React Native app by running:
```bash
expo init <YOUR_APP_NAME> --npm
```

For the purposes of this project, we'll use the name **Blurble**. Expo will create a directory called `Blurble` in your current directory with all the necessary packages.

Run `npm start` to start your development server. You can test your app on iOS and Android with the Expo Go app, or you can run the simulators by following the instructions on the server window.

In the `app/Blurble` directory, you'll see some base code for our app prewritten. React automatically generates some of this for us, but it also includes some custom code for the Blurble app. 

It's highly encouraged to go through the [React Native documentation](https://reactnative.dev/docs/getting-started) to understand how to use and build apps with React Native. We won't be covering the the specifics of front end developing using React Native in this tutorial, but a lot of resources can be found here, and just by Googling. 

## Step 2: Linking the the API and the React Native app

Now that we have a functional frontend and backend, it's time to link the two together! Luckily, React Native makes it easy to send HTTP requests by utilizing [Javscript's Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) in its framework. This means that there's no special code for sending requests in your React Native app as compared to a traditional web app, it's all compatible!

Let's create a function that will send requests to our API and return the its response. We'll call this function `getBlurbles`.
```ts
const HOST_ADDR: str = 'http://localhost:5000/';
 
/**
 * Asynchronously fetches a blurble from the API
 * at the designated endpoint.
 * @returns {object} A json object containing a list of Blurbles
 * @throws {Error} If the request fails
 */
const getBlurbles = async () => {
    try {
        const response = await fetch(`${HOST_ADDR}`);
        const json = await response.json();
        return json;
    } catch (error) {
        console.error(error);
    }
};
```

So what exactly is going on here? 
  - First, we're using the `fetch` function to make a request to the IP address and port of our API. For now, we're running the API on our local machine, so the address and port is `http://localhost:5000/` (or `http://127.0.0.1:5000/`).
  - Next, we want to gather the response from the API. The `await` keyword makes sure that the request is 
  completed before we continue. 
  - Next, we'll use the `json` function to parse the response into a json object, and return it for use in our code.
  - Finally, we'll throw an error if the request fails.

Theoretically, this should be all that's necessary to sucessfully get a response from our API. However, you may run into some issues with [Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). Luckily, the `flask-cors` package we installed earlier will help us handle this. Refer to the `api/bundle_api.py` file to see how.

So now that we can get Blurbles, how do we post them to the API and store them in our database?

Take a look at the code in `app/Blurble/App.tsx` to see how we handle posting to our API, and how we handle our response from the API to create to React Native components and display them on the screen.

Once you understand the code, run your React Native dev server with `npm start`, and try posting to the API. You should see your Blurble appear in the list of Blurbles. Make sure that your Flask API and Postgres database are running.

**Note:** If you attempt to connect to the API from your iPhone/Android device on Yale wifi, you may run into trouble connecting to `localhost`. For testing purposes, you can run your app in a web browser and test there, then move your API and database onto an AWS instance or another alternative to test on a device. If you can find a way to ensure your phone is on the same network as your API and database, you can test your app on your phone.

## Step 3: Testing your app!

By now, you should have a working React Native app that can post to the API and store the Blurbles in your database.

It's a good idea to write some tests for your app. You should probably test your API, and your frontend. 

When working in a team setting, Continuous Integration (CI) is a great way to test your app.

## Appendix/Helpful Notes

### Installation
 - You can install the python dependencies for this tutorial by running `pip install -r requirements.txt` in your virtual environment. 

### Maintainance
Make sure to stop your Postgres session when you're done by running:

```bash
pg_ctl -D /usr/local/var/postgres -l logfile stop # Stops the postgresql server
brew services stop postgresql # Alternatively, if installed through Homebrew.
```



