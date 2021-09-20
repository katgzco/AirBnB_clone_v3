#!/usr/bin/python3
""" New view for Users objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, make_response, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Return all the elements of User"""
    all_elements = storage.all(User)
    objects_list = []
    for states in all_elements.values():
        objects_list.append(states.to_dict())
    return jsonify(objects_list)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """ Return one element of User matched with id"""
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def users_id_delete(user_id):
    """ Delete one element of User matched with id"""
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_useres():
    """ Create a new User"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    else:
        variable = request.get_json(request.data)
        if 'email' not in variable.keys():
            abort(400, 'Missing email')
        if 'password' not in variable.keys():
            abort(400, 'Missing password')
        instance = User(**variable)  # Possible bug
        storage.new(instance)
        storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_users(user_id):
    """  one element of User matched with id"""
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    else:
        if not request.get_json():
            abort(400, 'Not a JSON')
        else:
            variable = request.get_json(request.data)
            for key, value in variable.items():
                if key not in ['email', 'id', 'created_at', 'updated_at']:
                    object[key] = value
            storage.save()
    return jsonify(object.to_dict()), 200
