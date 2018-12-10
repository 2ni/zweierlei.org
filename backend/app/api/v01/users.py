# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse

from app import db
from app.utils.dict import (filter_dict, merge_dict, exclude_dict, check_mandatory_fields)
from pprint import pprint

from redis.exceptions import WatchError

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)

import re

# from app.decorators import auth

class ApiTest(Resource):
    """
    Playground api
    """
    endpoint_url = ["/foo", "/bar"]

    def post(self):
        endpointUsed = re.sub("^.*?([^/]*)$", r"\1", request.path)
        resp =  jsonify({"msg": "ok", "endpoint": endpointUsed})
        resp.status_code = 201
        return resp

class ApiUsers(Resource):
    """
    http -F GET :5000/api/v0.1/users Authorization:"Bearer <jwt>"
    http -F GET :5000/api/v0.1/users/5834578e-351c-451a-94c6-500aa755f804 Authorization:"Bearer <jwt>"
    http -F POST :5000/api/v0.1/users Authorization:"Bearer <jwt>" email="foobar@zweierlei.org" firstname="Foo"

    """
    endpoint_url = ["/users", "/users/<uid>"]
    exposedFields = ["email", "firstname", "lastname"]
    # msg, uid are generated

    @jwt_required
    def get(self, uid=None):
        # method = getattr(self, uid, None)

        if uid and not self.is_allowed(uid):
            return make_response(jsonify({"msg": "not allowed"}), 403)

        rawData = self.get_userdata(uid)
        filteredData = filter_dict(rawData, self.exposedFields)
        return jsonify(merge_dict(filteredData, {"uid": rawData["uid"], "msg": "ok"}))

    @jwt_required
    def post(self, uid=None):
        """
        update user data in backend
        @return success/failure
        """

        rawNewData = request.json or {}
        # only exposed data allowed to start, keep password from current data
        dataToSave = filter_dict(rawNewData, self.exposedFields)

        # mandatory fields
        # TODO check if email not empty and is a potential email
        err = check_mandatory_fields(dataToSave, "email")
        if err:
            return make_response(jsonify(err), 400)

        if uid and not self.is_allowed(uid):
            return make_response(jsonify({"msg": "not allowed"}), 403)


        curRawData = self.get_userdata(uid)

        dataToSave["uid"] = curRawData.get("uid")
        # safety check, should never happen
        if not dataToSave["uid"]:
            return make_response(jsonify({"msg": "uid missing"}), 422)


        # password handling: keep old one if none given
        newPassword = rawNewData.get("password")
        if newPassword:
            dataToSave["password"] = sha256.hash(newPassword)
        else:
            dataToSave["password"] = curRawData.get("password")


        # TODO merge with duplicate code in auth.py
        args = []
        for k, v in dataToSave.items():
            args.append(k)
            args.append(v)

        ret = db.replaceOrInsertUser(args=args).lower()

        if ret == "ok":
            return jsonify(merge_dict(filter_dict(dataToSave, self.exposedFields + ["uid"]), {"msg": "ok"}))
        else:
            return make_response(jsonify({"msg": "email already registered"}), 409)

    def is_allowed(self, uid):
        isAdmin = False
        if isAdmin or uid == get_jwt_identity():
            return True
        else:
            return False

    def get_userdata(self, uid):
        """
        get all user data from <uid>
        populates also uid in data even not stored in db
        """

        if not uid:
            uid = get_jwt_identity()

        return merge_dict(db.hgetall("z:users:{uid}".format(uid=uid)), {"uid": uid})


    # @auth()
    # def privateFunction(self):
    #   pass
