#!/usr/bin/python3
"""  """
from flask import Flask, jsonify
from api.v1.views import app_views

status = Flask(__name__)

@app_views.route('/status', strict_slashes=False)
def status():
    """ Return in JSON data"""
    data = {'status' : 'OK'}
    return jsonify(data)
