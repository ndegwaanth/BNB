#!/usr/bin/python3
"""app.py to link API"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a Flask application instance
app = Flask(__name__)

# Import blueprint app_views and register it to the Flask instance app
app.register_blueprint(app_views)


# Define a method to handle teardown_appcontext
@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
