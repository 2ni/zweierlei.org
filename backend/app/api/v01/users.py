# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response
from flask_restful import reqparse

from app import db
from app.utils.dict import (filter_dict, merge_dict, exclude_dict, check_mandatory_fields, dict2list)
from app.api.zweierleiresource import ZweierleiResource
from pprint import pprint

from redis.exceptions import WatchError

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required)

import re

# from app.decorators import auth

class ApiUsers(ZweierleiResource):
    """
    http -F GET :5000/api/v01/users Authorization:"Bearer <jwt>"
    http -F GET :5000/api/v01/users/5834578e-351c-451a-94c6-500aa755f804 Authorization:"Bearer <jwt>"
    http -F POST :5000/api/v01/users Authorization:"Bearer <jwt>" email="foobar@zweierlei.org" firstname="Foo"

    """
    endpoint_url = ["/users", "/users/<uid>"]
    exposed_fields = ["email", "firstname", "lastname"]
    # msg, uid are generated

    @fresh_jwt_required
    def get(self, uid=None):
        # method = getattr(self, uid, None)

        if uid and not self.is_allowed(uid):
            return self.response("not allowed")

        rawData = self.get_userdata(uid)
        filteredData = filter_dict(rawData, self.exposed_fields)
        return jsonify(merge_dict(filteredData, {"uid": rawData["uid"], "msg": "ok"}))

    @fresh_jwt_required
    def post(self, uid=None):
        """
        update user data in backend
        @return success/failure
        """

        rawNewData = request.json or {}
        # only exposed data allowed to start, keep password from current data
        dataToSave = filter_dict(rawNewData, self.exposed_fields)

        # mandatory fields
        # TODO check if email is a potential email
        err = check_mandatory_fields(dataToSave, "email")
        if err:
            return make_response(jsonify(err), 422)

        if uid and not self.is_allowed(uid):
            return self.response("not allowed")


        curRawData = self.get_userdata(uid)

        dataToSave["uid"] = curRawData.get("uid")
        # safety check, should never happen
        if not dataToSave["uid"]:
            self.response("missing", "uid")


        # password handling: keep old one if none given
        newPassword = rawNewData.get("password")
        if newPassword:
            dataToSave["password"] = sha256.hash(newPassword)
        else:
            dataToSave["password"] = curRawData.get("password")

        ret = db.replaceOrInsertUser(args=dict2list(dataToSave)).lower()

        if ret == "ok":
            return jsonify(merge_dict(filter_dict(dataToSave, self.exposed_fields + ["uid"]), {"msg": "ok"}))
        else:
            return self.response(*ret.split(":"))

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
