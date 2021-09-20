#!/usr/bin/python3
""" New view for City objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, request, make_response, abort

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ Return the list of all cities"""
    all_objects = storage.all(City)
    cities_list = []
    for cities in all_objects.values():
        if  state_id == cities.state_id:
            cities_list.append(cities.to_dict())
        if cities_list is None:
            abort(404)
    return jsonify(cities_list)
