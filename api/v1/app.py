#!/usr/bin/python3
"""  """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)


if getenv("HBNB_API_HOST") is None:
    HBNB_API_HOST = '0.0.0.0'
else:
    HBNB_API_HOST = getenv("HBNB_API_HOST")

if getenv("HBNB_API_PORT") is None:
    HBNB_API_PORT = '5000'
else:
    HBNB_API_PORT = getenv("HBNB_API_PORT")



app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"originis": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    error = {"error": "Not found"}
    return make_response(jsonify(error), 404)


@app.teardown_appcontext
def store_close(exception):
    """Clossing session"""
    storage.close()


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
