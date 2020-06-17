import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from sys import exc_info

# ----------------------------------------------------------------------------#
# App Setup
# ----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'http://localhost:5000/'
    header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
    header['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
    return response

# db_drop_and_create_all()

# ----------------------------------------------------------------------------#
# Custom Functions
# ----------------------------------------------------------------------------#


def get_error_message(error, default_text):
    try:
        # Return message contained in error, if possible
        return error['description']
    except TypeError:
        # otherwise, return given default text
        return default_text


def get_all_drinks(recipe_format):
    # Get all drinks in database
    all_drinks = Drink.query.order_by(Drink.id).all()
    # Format with different recipe detail level
    if recipe_format.lower() == 'short':
        all_drinks_formatted = [drink.short() for drink in all_drinks]
    elif recipe_format.lower() == 'long':
        all_drinks_formatted = [drink.long() for drink in all_drinks]
    else:
        return abort(500, {'message': 'bad formatted function call'})

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'No drinks found in Database.'})

    # Return formatted list of drinks
    return all_drinks_formatted


# ----------------------------------------------------------------------------#
# Endpoints                                                                  #
# ----------------------------------------------------------------------------#

@app.route('/drinks', methods=['GET'])
def drinks():
    return jsonify({
        'success': True,
        'drinks': get_all_drinks('short')
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    return jsonify({
        'success': True,
        'drinks': get_all_drinks('long')
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        new_drink_data = json.loads(request.data.decode('utf-8'))
        new_drink = Drink(title=new_drink_data['title'], recipe=json.dumps(new_drink_data['recipe']))
        Drink.insert(new_drink)
        drinks = list(map(Drink.long, Drink.query.all()))
        result = {
            "success": True,
            "drinks": drinks
        }
        return jsonify(result)
    except exc.SQLAlchemyError:
        abort(422)
    except Exception:
        abort(503)        


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    try:
        # Get body from request
        body = request.get_json()

        if not body:
            exc_info(400, {'message': 'request does not contain a valid JSON body.'})

        # Find drink which should be updated by id
        drink_to_update = Drink.query.filter(Drink.id == drink_id).one_or_none()

        # Check if and which fields should be updated
        updated_title = body.get('title', None)
        updated_recipe = body.get('recipe', None)

        # Depending on which fields are available, make apropiate updates
        if updated_title:
            drink_to_update.title = body['title']

        if updated_recipe:
            drink_to_update.recipe = """{}""".format(body['recipe'])

        drink_to_update.update()

        return jsonify({
            'success': True,
            'drinks': [Drink.long(drink_to_update)]
        })
    except exc.SQLAlchemyError:
        abort(422)    


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    try:
        """Deletes 1 drink with given id"""
        if not drink_id:
            abort(422, {'message': 'Please provide valid drink id'})

        # Get drink with id
        drink_to_delete = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if not drink_to_delete:
            abort(404,{'message': 'Drink with id {} not found'.format(drink_id)})

        drink_to_delete.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except exc.SQLAlchemyError:
        abort(503)    


# ----------------------------------------------------------------------------#
# Error Handlers                                                             #
# ----------------------------------------------------------------------------#

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": get_error_message(error, "Unprocessable")
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": get_error_message(error, "Resource not found")
    }), 400


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": get_error_message(error, "Resource not found")
    }), 404


@app.errorhandler(AuthError)
def authentication_failed(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": get_error_message(auth_error.error, "Authentication failed")
    }), 401


@app.errorhandler(500)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": get_error_message(error, "Internal Server Error")
    }), 500
