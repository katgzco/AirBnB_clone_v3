#!/usr/bin/python3
""" New view for City objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, request, make_response, abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """ Return the list of all Places"""
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    all_objects = storage.all(Place)
    related_list = []
    for obj in all_objects.values():
        if city_id == obj.city_id:
            related_list.append(obj.to_dict())
    return jsonify(related_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ Return one element of Place matched with id"""
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_id_delete(place_id):
    """ Delete one element of Place matched with id"""
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places(city_id):
    """ Create a new Place"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    else:
        object = storage.get(City, city_id)
        if object is None:
            abort(404)
        variable = request.get_json(request.data)
        if 'user_id' not in variable.keys():
            abort(400, 'Missing email')
        if not storage.get(User, variable['user_id']):
            abort(404)
        if 'name' not in variable.keys():
            abort(400, 'Missing name')
        instance = Place(city_id=city_id, **variable)
        storage.new(instance)
        storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """  one element of Place matched with id"""
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    else:
        if not request.get_json():
            abort(400, 'Not a JSON')
        else:
            variable = request.get_json(request.data)
            for key, value in variable.items():
                if key not in ['user_id', 'id', 'city_id',
                               'updated_at', 'created_at']:
                    setattr(object, key, value)
            storage.save()
    return jsonify(object.to_dict()), 200
