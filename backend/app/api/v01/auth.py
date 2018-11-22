# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response, current_app
from flask_restful import Resource, reqparse

from app import db
from app.utils.dict import (filter_dict, merge_dict, check_mandatory_fields)
from pprint import pprint

from redis.exceptions import WatchError

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_jti, get_raw_jwt)

import re, uuid

# from app.decorators import auth

class ApiLogin(Resource):
    """
    submit creds to backend.
    http -F POST :5000/api/v0.1/login email=test@test.com password=test

    @return success/failure, session token, profile info
    """
    endpoint_url = ["/login", "/register"]
    exposedFields = ["email", "firstname", "lastname"]

    def post(self):
        data = request.json or {}

        # mandatory fields
        err = check_mandatory_fields(data, ["email", "password"])
        if err:
            return make_response(jsonify(err), 400)

        endpointUsed = re.sub("^.*?([^/]*)$", r"\1", request.path)

        # login
        if (endpointUsed == "login"):
            # verify if email exists in db
            uid = db.get("z:usersByEmail:{email}".format(email=data["email"]))
            user = db.hgetall("z:users:{uid}".format(uid=uid)) if uid else {}
            # verify email/password
            if user and sha256.verify(data["password"], user["password"]):
                return self.login(uid, user)
            else:
                return self.response("password")

        # register
        else:
            dataFiltered = filter_dict(data, self.exposedFields)
            dataFiltered["password"] = sha256.hash(data["password"])
            uid = uuid.uuid4()
            with db.pipeline() as pipe:
                # ensure email does not yet exist
                emailKey = "z:usersByEmail:{email}".format(email=dataFiltered["email"])
                try:
                    pipe.watch(emailKey)
                    if pipe.exists(emailKey):
                        raise WatchError
                    else:
                        pipe.multi()
                        pipe.hmset("z:users:{uid}".format(uid=uid), dataFiltered)
                        pipe.sadd("z:allUsers", uid)
                        pipe.set(emailKey, uid)
                        pipe.execute()
                except WatchError:
                    pipe.reset()
                    return self.response("exists")
            return self.login(uid)

    def login(self, uid, user=None):
        access_token = create_access_token(identity = uid)
        refresh_token = create_refresh_token(identity = uid)
        user = db.hgetall("z:users:{uid}".format(uid=uid)) if user == None else user

        # store tokens in db for security and logout blacklisting
        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)

        db.set("z:tokens:{jti}".format(jti=access_jti), "false", current_app.config.get("ACCESS_EXPIRES") * 1.2)
        db.set("z:tokens:{jti}".format(jti=refresh_jti), "false", current_app.config.get("REFRESH_EXPIRES") * 1.2)

        return jsonify(merge_dict(
            filter_dict(user, self.exposedFields),
            {
                "msg": "ok",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "uid": uid
            }
        ));

    def response(self, type):
        respErrs = {
            "password": make_response(jsonify({"msg": "bad email/password"}), 401),
            "exists": make_response(jsonify({"msg": "email already registered"}), 409)
        }
        return respErrs[type]

class ApiLogoutAccess(Resource):
    """
    https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/redis_blacklist.py

    revoke access token
    @return success/failure
    """
    endpoint_url = ["/revoke_access"]

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        db.set("z:tokens:{jti}".format(jti=jti), "true", current_app.config.get("ACCESS_EXPIRES") * 1.2)
        return jsonify({"msg": "access token revoked"})

class ApiLogoutRefresh(Resource):
    """
    https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/redis_blacklist.py

    revoke refresh token
    @return success/failure
    """
    endpoint_url = ["/revoke_refresh"]

    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        db.set("z:tokens:{jti}".format(jti=jti), "true", current_app.config.get("REFRESH_EXPIRES") * 1.2)
        return jsonify({"msg": "refresh token revoked"})


class ApiRefresh(Resource):
    """
    endpoint to refresh access token with the refresh token

    http -F GET :5000/api/v0.1/refresh Authorization:"Bearer <refresh_token>"
    """
    endpoint_url = ["/refresh"]

    @jwt_refresh_token_required
    def post(self):
        current = get_jwt_identity()
        access_token = create_access_token(identity = current)
        access_jti = get_jti(encoded_token=access_token)
        db.set("z:tokens:{jti}".format(jti=access_jti), "false", current_app.config.get("ACCESS_EXPIRES") * 1.2)

        return jsonify({"access_token": access_token})
