#!/usr/bin/python3
'''Contains the city view for the API.'''
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """Retrieves a city object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    else:
        return jsonify(city_obj.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """Retrieves the list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify([city.to_dict() for city in state.cities])


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    req = request.get_json()
    obj = City(**req)
    setattr(obj, 'state_id', state_id)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
