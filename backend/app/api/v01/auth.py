# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response, current_app
from flask_restful import reqparse

from app import db
from app.utils.dict import (filter_dict, merge_dict, check_mandatory_fields, dict2list)
from app.api.zweierleiresource import ZweierleiResource
from pprint import pprint

from redis.exceptions import WatchError

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_jti, get_raw_jwt)

import re, uuid

# from app.decorators import auth

class ApiLogin(ZweierleiResource):
    """
    submit creds to backend.
    http -F POST :5000/api/v01/login email=test@test.com password=test

    @return success/failure, session token, profile info
    """
    endpoint_url = ["/login", "/register"]
    exposedFields = ["email", "firstname", "lastname"]

    def post(self):
        """
        http -F POST :5000/api/v01/login email=test@zweierlei.org password="test"
        http -F POST :5000/api/v01/register email=test@zweierlei.org password="test"
        """
        data = request.json or {}

        # mandatory fields
        errs = check_mandatory_fields(data, ["email", "password"])
        if errs:
            return make_response(jsonify(errs), 422)

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
                return self.response("wrong creds")

        # register
        else:
            # verify email by simple validation for now
            # https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
            match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", data["email"])
            if match == None:
                return self.response("wrong format", "email")

            dataFiltered = filter_dict(data, self.exposedFields)
            dataFiltered["password"] = sha256.hash(data["password"])
            dataFiltered["uid"] = uuid.uuid4()

            ret = db.replaceOrInsertUser(args=dict2list(dataFiltered)).lower()
            if ret == "ok":
                return self.login(dataFiltered["uid"])
            else:
                return self.response(*ret.split(":"))

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

class ApiLogoutAccess(ZweierleiResource):
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

class ApiLogoutRefresh(ZweierleiResource):
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


class ApiRefresh(ZweierleiResource):
    """
    endpoint to refresh access token with the refresh token

    http -F GET :5000/api/v01/refresh Authorization:"Bearer <refresh_token>"
    """
    endpoint_url = ["/refresh"]

    @jwt_refresh_token_required
    def post(self):
        current = get_jwt_identity()
        access_token = create_access_token(identity = current)
        access_jti = get_jti(encoded_token=access_token)
        db.set("z:tokens:{jti}".format(jti=access_jti), "false", current_app.config.get("ACCESS_EXPIRES") * 1.2)

        return jsonify({"msg": "ok", "access_token": access_token})
