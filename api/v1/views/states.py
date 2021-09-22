#!/usr/bin/python3
""" Create a new view for State
objects that handles all default RESTFul API actions"""

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def consult_create():
    """View function handling GET and PUT requests"""

    if request.method == 'GET':
        all_states = storage.all(State)
        states_list = []
        for obj in all_states.values():
            states_list.append(obj.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        request_data = request.get_json()
        if 'name' not in request_data.keys():
            abort(400, 'Missing name')
        instance = State(**request_data)
        instance.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def consult_delete_update(state_id):

    object = storage.get(State, state_id)
    if object is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(object.to_dict())

    if request.method == 'DELETE':
        storage.delete(object)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        request_data = request.get_json()
        if 'name' not in request_data.keys():
            abort(400, 'Missing name')
        setattr(object, 'name', request_data.get('name'))
        object.save()
    return jsonify(object.to_dict()), 200
