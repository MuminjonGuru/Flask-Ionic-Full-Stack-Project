import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Setup
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)
# db_drop_and_create_all()

#----------------------------------------------------------------------------#
# Custom Functions
#----------------------------------------------------------------------------#

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
        return abort(500, {'message': 'bad formatted function call. recipe_format needs to be "short" or "long".'})

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'No drinks found in Database.'})
    
    # Return formatted list of drinks
    return all_drinks_formatted

#----------------------------------------------------------------------------#
# Endpoints                                                                  #
#----------------------------------------------------------------------------#

@app.route('/drinks' , methods=['GET'])
def drinks():
    return jsonify({
    'success': True,
    'drinks': get_all_drinks('short')
    })

@app.route('/drinks-detail',  methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    return jsonify({
        'success': True,
        'drinks': get_all_drinks('long')
    }), 200

@app.route('/drinks',  methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()
    new_drink = Drink(title = body['title'], recipe = """{}""".format(body['recipe']))
    
    new_drink.insert()
    new_drink.recipe = body['recipe']
    return jsonify({
        'success': True,
        'drinks': Drink.long(new_drink)
    }), 200
    
@app.route('/drinks/<int:drink_id>',  methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    # Get body from request
    body = request.get_json()

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    
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

@app.route('/drinks/<int:drink_id>',  methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    """Deletes 1 drink with given id"""
    if not drink_id:
        abort(422, {'message': 'Please provide valid drink id'})

    # Get drink with id
    drink_to_delete = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink_to_delete:
        abort(404, {'message': 'Drink with id {} not found in database.'.format(drink_id)})
     
    drink_to_delete.delete()
    
    return jsonify({
        'success': True,
        'delete': drink_id
    })

#----------------------------------------------------------------------------#
# Error Handlers                                                             #
#----------------------------------------------------------------------------#

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": get_error_message(error,"Unprocessable")
                    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": get_error_message(error, "Resource not found")
                    }), 400

@app.errorhandler(404)
def ressource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": get_error_message(error, "Resource not found")
                    }), 404

@app.errorhandler(AuthError)
def authentification_failed(AuthError): 
    return jsonify({
                    "success": False, 
                    "error": AuthError.status_code,
                    "message": get_error_message(AuthError.error, "Authentification failed")
                    }), 401