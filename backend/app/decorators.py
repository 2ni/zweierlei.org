# -*- coding: utf-8 -*-

from functools import update_wrapper
from flask import current_app, request, jsonify
from app.user import User, UserSchema

import uuid

def auth(ret_creds=False):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):

			auth_header = request.headers.get("Authorization")
			auth_token = auth_header.split(" ")[1] if auth_header else ""

			if not auth_token:
				return jsonify({"success": False, "msg": "You need to be logged in to access this ressource"})

			id = User.decode_auth_token(auth_token)

			# in case of invalid/expired token -> id is a string (see user.py decode_auth_token)
			if isinstance(id, str):
				return jsonify({"success": False, "msg": id})

			user_db = current_app.config["USERS_COLLECTION"].find_one({"_id": uuid.UUID(id)})

			if not user_db:
				return jsonify({"success": False, "msg":"User not found"})

			if not ret_creds:
				return fn(*args, **kwargs)

			schema = UserSchema(exclude=("", "password")) #TODO if only password excluded, it shows all data?!?
			validated_data, errors = schema.dump(user_db)
			return jsonify({"success": True, "data": validated_data})

        return update_wrapper(wrapped_function, fn)
    return decorator
