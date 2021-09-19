#!/usr/bin/python3
""" Create a new view for State
objects that handles all default RESTFul API actions"""

from models import storage
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Return all the elements of State"""
    all_elements = storage.all(State)
    states_list = []
    for states in all_elements.values():
        states_list.append(states.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """ Return one element of State matched with id"""
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/states/<state_id>',
                methods=['DELETE'], strict_slashes=False)
def states_id_delete(state_id):
    """ Return one element of State matched with id"""
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a new State"""
    if request.is_json:
        variable = request.get_json(request.data)
        if 'name' in variable.keys():
            instance = State(name = variable['name'])
            storage.new(instance)
            storage.save()
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """  one element of State matched with id"""
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    else:
        if request.is_json:
            variable = request.get_json(request.data)
            if 'name' in variable.keys():
                object.name = variable['name']
                storage.save()
            else:
                abort(400, 'Not a JSON')
    return jsonify(object.to_dict()), 200
