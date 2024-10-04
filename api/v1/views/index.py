#!/usr/bin/python3
"""Route handler for the HBNB API."""
from flask import jsonify
from api.v1.views import app_views
from models import storage

entity_mapping = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User",
}


@app_views.route("/status", strict_slashes=False)
def get_status():
    """Endpoint to check the API status."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """Endpoint to retrieve statistics for each entity."""
    stats = {}
    for entity, model in entity_mapping.items():
        stats[entity] = storage.count(model)
    return jsonify(stats)


if __name__ == "__main__":
    pass
