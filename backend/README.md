# Coffee Shop - Backend 📡

  

## Getting Started

  

### Installing Dependencies

  

#### Python 3.7

  

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

  

#### Virtual Enviornment

  

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Or just create it by using this command:
```bash
py -m venv env 
```
env is the name of the environment you can give your desired name to that.

To activate/run the environment you can utilize this command
```bash
.\env\Scripts\activate
```

Now you are good to go!
  

#### PIP Dependencies

  

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

  

```bash

pip install -r requirements.txt

```

Also be sure to install python-dotenv to use .env files (if you want)
```bash
pip install python-dotenv
```
  

This will install all of the required packages we selected within the `requirements.txt` file.

  

##### Key Dependencies

  

-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

  

-  [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

  

-  [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

  

## Running the server

  

From within the `./src` directory first ensure you are working using your created virtual environment.

  

Each time you open a new terminal session, run:

  

```bash

export FLASK_APP=api.py;

```
Or if you are using PowerShell or CMD in Windows OS you can utilize this command
```bash
$env:FLASK_APP="api.py"
```


  

To run the server, execute:

  

```bash

flask run --reload

```

  

The `--reload` flag will detect file changes and restart the server automatically.

## Routes
```
@app.route('/drinks', methods=['GET'])
- Shows the drinks list


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
- Get all drinks


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
- Add a new drink (item) to the database


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
- Update/Edit/Patch the drink in the DB


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
- Deletes 1 drink with given id

```

## auth.py
```
Be sure to update these values with your own environment variables on .env file!
- AUTH0_DOMAIN = 'name.auth0.com'
- ALGORITHMS = ['type']
- API_AUDIENCE = 'audience name'
```


## Tasks - Completed!

  

### Setup Auth0

  

1. Create a new Auth0 Account

2. Select a unique tenant domain

3. Create a new, single page web application

4. Create a new API

- in API Settings:

- Enable RBAC

- Enable Add Permissions in the Access Token

5. Create new API permissions:

- `get:drinks-detail` - Shows all the drinks which are stored in the DB (in this one SQLite DB)

- `post:drinks` - To add a new drink item to the database which will be given to Manager role

- `patch:drinks` - To update/edit drink in the list

- `delete:drinks` - To remove a drink from the database

6. Create new roles for:

- Barista

- can `get:drinks-detail`

- Manager

- can perform all actions

7. Test your endpoints with [Postman](https://getpostman.com).

- Register 2 users - assign the Barista role to one and Manager role to the other.

- Sign into each account and make note of the JWT.

- Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`

- Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).

- Run the collection and correct any errors.

- Export the collection overwriting the one we've included so that we have your proper JWTs during review!

  

### Implement The Server

  

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

  

1. `./src/auth/auth.py`

2. `./src/api.py`
