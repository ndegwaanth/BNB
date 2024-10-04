#!/usr/bin/python3
"""amenities_handler.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


def fetch_all_amenities():
    """Retrieve all amenities."""
    return [amenity.to_dict() for amenity in storage.all("Amenity").values()]


def fetch_amenity(amenity_id):
    """Retrieve a specific amenity by its ID."""
    return storage.get("Amenity", amenity_id)


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def list_amenities():
    """Fetches information for all amenities."""
    return jsonify(fetch_all_amenities())


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["GET"], strict_slashes=False
)
def retrieve_amenity(amenity_id):
    """Fetches details of a specific amenity."""
    amenity = fetch_amenity(amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["DELETE"], strict_slashes=False
)
def remove_amenity(amenity_id):
    """Deletes an amenity based on the given amenity ID."""
    amenity = fetch_amenity(amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new amenity."""
    json_data = request.get_json()
    if json_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    name = json_data.get("name")
    if name is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**json_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Updates an existing amenity."""
    amenity = fetch_amenity(amenity_id)
    if amenity is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
