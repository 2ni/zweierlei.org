# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse

from app import db
from app.utils.dict import (filter_dict, merge_dict, exclude_dict, check_mandatory_fields)
from pprint import pprint

from redis.exceptions import WatchError

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)

import re, uuid

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
    http :5000/api/v0.1/users
    http -F :5000/v0.1/api/users/ http -F GET :5000/api/v0.1/users/5834578e-351c-451a-94c6-500aa755f804 Authorization:'Bearer <jwt>'
    """
    endpoint_url = ["/users", "/users/<uid>"]
    exposedFields = ["email", "firstname", "lastname"]
    # msg, uid are generated

    @jwt_required
    def get(self, uid=None):
        # method = getattr(self, uid, None)

        rawData = self.get_user(uid)
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
        dataToSave = filter_dict(rawNewData, self.exposedFields + ["password"])

        # mandatory fields
        # TODO check if email not empty and is a potential email
        err = check_mandatory_fields(dataToSave, "email")
        if err:
            return make_response(jsonify(err), 400)

        curData = self.get_user(uid)

        uid = curData.get("uid")
        # safety check, should never happen
        if not uid:
            return make_response(jsonify({"msg": "missing uid"}), 422)

        # (new) password is given
        newPassword = rawNewData.get("password")
        if newPassword:
            dataToSave["password"] = sha256.hash(newPassword)

        newEmail = rawNewData.get("email")
        curEmail = curData.get("email")
        # new email means we have to update some more stuff
        if newEmail != curEmail:
            with db.pipeline() as pipe:
                pipe.multi()
                pipe.hmset("z:users:{uid}".format(uid=uid), dataToSave)
                pipe.set("z:usersByEmail:{email}".format(email=newEmail), uid)
                pipe.delete("z:usersByEmail:{email}".format(email=curEmail))
                pipe.execute()
        else:
            db.hmset("z:users:{uid}".format(uid=uid), dataToSave)

        return jsonify(merge_dict(filter_dict(dataToSave, self.exposedFields), {"uid": uid, "msg": "ok"}))

    def get_user(self, uid):
        """
        get all user data from <uid>
        populates also uid in data even not stored in db
        """
        isAdmin = False
        if (uid and isAdmin):
            uidLookup = uid
        else:
            uidLookup = get_jwt_identity()

        return merge_dict(db.hgetall("z:users:{uid}".format(uid=uidLookup)), {"uid": uidLookup})


    # @auth()
    # def privateFunction(self):
    #   pass
