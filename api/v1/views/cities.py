#!/usr/bin/python3
""" New view for City objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, request, make_response, abort


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ Return the list of all cities"""
    all_objects = storage.all(City)
    cities_list = []
    for cities in all_objects.values():
        if state_id == cities.state_id:
            cities_list.append(cities.to_dict())
        if cities_list is None:
            abort(404)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """ Return one element of City matched with id"""
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def cities_id_delete(city_id):
    """ Delete one element of City matched with id"""
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_cities(state_id):
    """ Create a new State"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    else:
        object = storage.get(State, state_id)
        if object is None:
            abort(404)
        variable = request.get_json(request.data)
        if 'name' in variable.keys():
            instance = City(state_id=state_id, name=variable['name'])
            storage.new(instance)
            storage.save()
        else:
            abort(400, 'Missing name')
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """one element of State matched with id"""
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    else:
        if not request.get_json():
            abort(400, 'Not a JSON')
        else:
            variable = request.get_json(request.data)
            if 'name' in variable.keys():
                object.name = variable['name']
                storage.save()
            else:
                abort(400, 'Missing name')
    return jsonify(object.to_dict()), 200
