#!/usr/bin/python3
"""contains the paths and views used by the server"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

status = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """ Return in JSON data"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Return in JSON data"""
    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}

    count_class = dict()

    for clas, objclass in classes.items():
        count_class.update({clas: storage.count(objclass)})

    return jsonify(count_class)
