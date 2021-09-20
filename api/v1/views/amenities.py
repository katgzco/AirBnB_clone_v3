#!/usr/bin/python3
""" New view for Amenities objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Return all the elements of Amenity"""
    all_elements = storage.all(Amenity)
    states_list = []
    for states in all_elements.values():
        states_list.append(states.to_dict())
    return jsonify(states_list)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_id(amenity_id):
    """ Return one element of Amenity matched with id"""
    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenities_id_delete(amenity_id):
    """ Delete one element of Amenity matched with id"""
    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """ Create a new Amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    else:
        variable = request.get_json(request.data)
        if 'name' in variable.keys():
            instance = Amenity(name=variable['name'])
            storage.new(instance)
            storage.save()
        else:
            abort(400, 'Missing name')
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenities(amenity_id):
    """  one element of Amenity matched with id"""
    object = storage.get(Amenity, amenity_id)
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
