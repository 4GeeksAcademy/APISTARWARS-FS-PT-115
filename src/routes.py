from flask import Flask, request, jsonify, Blueprint
from models import db, User, Character, Planets, PlanetFavs, CharacterFavs
from datetime import date


api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200


@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    required_fields = ["email", "password", "name"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_user = User(
        email=data["email"],
        password=data["password"],
        name=data["name"],
        date_resgister=date.today(),
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201


@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


# siguiente sin serialize()
@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "image": c.image,
        "data": c.data
    } for c in characters]), 200


@api.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    return jsonify({
        "id": character.id,
        "name": character.name,
        "image": character.image,
        "data": character.data
    }), 200


@api.route("/users/<int:user_id>/favorites/planets/<int:planet_id>", methods=["POST"])
def add_favorite_planet(user_id, planet_id):
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404

    if any(fav.planet_id == planet_id for fav in user.planet_favorites):
        return jsonify({"error": "Planet already in favorites"}), 409

    fav = PlanetFavs(planet_id=planet_id)
    user.planet_favorites.append(fav) 
    db.session.commit()

    return jsonify({"msg": f"Planet '{planet.name}' added to favorites"}), 201

@api.route("/users/<int:user_id>/favorites/characters/<int:character_id>", methods=["POST"])
def add_favorite_character(user_id, character_id):
    
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    if any(fav.character_id == character_id for fav in user.character_favorites):
        return jsonify({"error": "Character already in favorites"}), 409

    fav = CharacterFavs(character_id=character_id)
    user.character_favorites.append(fav) 
    db.session.commit()

    return jsonify({"msg": f"Character '{character.name}' added to favorites"}), 201

@api.route("/users/<int:user_id>/favorites/planets/<int:planet_id>", methods=["DELETE"])
def remove_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404

    for fav in user.planet_favorites:
        if fav.planet_id == planet_id:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({"msg": f"Planet '{planet.name}' removed from favorites"}), 200

    return jsonify({"error": "Planet not in favorites"}), 404

@api.route("/users/<int:user_id>/favorites/characters/<int:character_id>", methods=["DELETE"])
def remove_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    for fav in user.character_favorites:
        if fav.character_id == character_id:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({"msg": f"Character '{character.name}' removed from favorites"}), 200

    return jsonify({"error": "Character not in favorites"}), 404
