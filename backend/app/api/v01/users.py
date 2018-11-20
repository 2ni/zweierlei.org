# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse

from app import db
from pprint import pprint

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
        resp =  jsonify({"message": "ok", "endpoint": endpointUsed})
        resp.status_code = 201
        return resp

class ApiLogin(Resource):
    """
    submit creds to backend.
    http -F POST :5000/api/v0.1/login email=test@test.com password=test

    @return success/failure, session token, profile info
    """
    endpoint_url = ["/login", "/register"]
    allowedFields = ["email", "firstName", "lastName"]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("email", help="required element", required = True)
        self.reqparse.add_argument("password", help="required element", required = True)
        super(ApiLogin, self).__init__()

    def post(self):
        endpointUsed = re.sub("^.*?([^/]*)$", r"\1", request.path)
        data = self.reqparse.parse_args()
        uid = db.get("z:usersByEmail:{email}".format(email=data["email"]))

        # err = jsonify({"errors": "email/password mismatch"})
        # err.status_code = 401

        # login
        if (endpointUsed == "login"):
            err = make_response(jsonify({"errors": "email/password mismatch"}), 401)

            # verify if email exists in db
            if (uid):
                user = db.hgetall("z:users:{uid}".format(uid=uid))
                # verify email/password
                if sha256.verify(data["password"], user["password"]):
                    return self.login(uid, user)
                else:
                    return err
            else:
                return err
        # register
        else:
            if uid:
                return make_response(jsonify({"errors": "email already registered"}), 409)

            dataFiltered = { k: data[k] for k in self.allowedFields if k in data }
            dataFiltered["password"] = sha256.hash(data["password"])
            uid = uuid.uuid4()
            pipe = db.pipeline()
            pipe.hmset("z:users:{uid}".format(uid=uid), dataFiltered)
            pipe.sadd("z:allUsers", uid)
            pipe.set("z:usersByEmail:{email}".format(email=dataFiltered["email"]), uid)
            pipe.execute()
            return self.login(uid)

    def login(self, uid, user=None):
        access_token = create_access_token(identity = uid)
        refresh_token = create_refresh_token(identity = uid)
        user = db.hgetall("z:users:{uid}".format(uid=uid)) if user == None else user
        return jsonify(
            **{ k: user[k] for k in self.allowedFields if k in user },
            **{
                "message": "ok",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        );


class ApiLogout(Resource):
    """
    execute logout in backend.
    @return success/failure
    """
    endpoint_url = ["/logout"]



class ApiUsers(Resource):
    """
    http :5000/api/v0.1/users
    http -F :5000/v0.1/api/users/ http -F GET :5000/api/v0.1/users/5834578e-351c-451a-94c6-500aa755f804 Authorization:'Bearer <jwt>'
    """
    endpoint_url = ["/users", "/users/<uid>"]
    allowedFields = ["email", "firstName", "lastName"]

    @jwt_required
    def get(self, uid=None):
        # method = getattr(self, uid, None)

        isAdmin = False
        if (uid and isAdmin):
            uidLookup = uid
        else:
            uidLookup = get_jwt_identity()

        user = db.hgetall("z:users:{uid}".format(uid=uidLookup))
        userFiltered = { k: user[k] for k in self.allowedFields if k in user }
        return jsonify(userFiltered)

        """
        http://flask.pocoo.org/snippets/71/

        event = db.hgetall(path)
        event["ttl"] = db.ttl(path)
        #cast integers accordingly, nested arrays, dicts not supported for now  :(
        dict_with_ints = dict((k,int(v) if isInt(v) else v) for k,v in event.iteritems())
        return json.dumps(dict_with_ints), 200

        p = db.pipeline()
        p.sadd...
        p.execute()
        """

        return jsonify({"msg": "test uid <{uid}>".format(uid=uid)})

    def post(self, uid):
        """
        update user data in backend
        @return success/failure
        """
        user = db.hgetall("z:users:5834578e-351c-451a-94c6-500aa755f804")
        return jsonify(uid)

    # @auth()
    # def privateFunction(self):
    #   pass
