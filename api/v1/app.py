#!/usr/bin/python3

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

if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
