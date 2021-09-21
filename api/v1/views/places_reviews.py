#!/usr/bin/python3
""" New view for City objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from flask import jsonify, request, make_response, abort


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_list(place_id):
    """ Return all reviews list """
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    all_objects = storage.all(Review)
    related_list = []
    for obj in all_objects.values():
        if place_id == obj.place_id:
            related_list.append(obj.to_dict())
    return jsonify(related_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """ Return one element of Review matched with id"""
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_id_delete(review_id):
    """ Delete one element of Review matched with id"""
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """ Create a new Place"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    else:
        object = storage.get(Place, place_id)
        if object is None:
            abort(404)
        variable = request.get_json(request.data)
        if 'user_id' not in variable.keys():
            abort(400, 'Missing email')
        if not storage.get(User, variable['user_id']):
            abort(404)
        if 'text' not in variable.keys():
            abort(400, 'Missing text')
        instance = Review(place_id=place_id, **variable)
        storage.new(instance)
        storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """  one element of Place matched with id"""
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    else:
        if not request.get_json():
            abort(400, 'Not a JSON')
        else:
            variable = request.get_json(request.data)
            for key, value in variable.items():
                if key not in ['user_id', 'id', 'place_id',
                               'updated_at', 'created_at']:
                    setattr(object, key, value)
            storage.save()
    return jsonify(object.to_dict()), 200
