# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import Resource, reqparse

from app import db
from pprint import pprint

import re

# from app.decorators import auth

class ApiRegister(Resource):
    """
    submit registration to backend
    @return success/failure. If success same as login
    """
    endpoint_url = ["/register", "/foobar"]

    def post(self):
        return jsonify({"message": "ok", "path": re.sub("^.*?([^/]*)$", r"\1", request.path)})


class ApiLogin(Resource):
    """
    submit creds to backend.
    @return success/failure, session token, profile info
    """
    endpoint_url = ["/login"]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", help="required element", required = True)
        self.reqparse.add_argument("password", help="required element", required = True)
        super(ApiLogin, self).__init__()

    def post(self):
        data = self.reqparse.parse_args()
        print(data)
        return jsonify(data)

class ApiLogout(Resource):
    """
    execute logout in backend.
    @return success/failure
    """
    endpoint_url = ["/logout"]



class ApiUsers(Resource):
    """
    http :5000/api/v0.1/users
    http -F :5000/v0.1/api/users/
    """
    endpoint_url = ["/users", "/users/<uid>"]

    def get(self, uid=None):
        # method = getattr(self, uid, None)

        user = db.hgetall("z:users:5834578e-351c-451a-94c6-500aa755f804")
        return jsonify(user)

        # return jsonify({"stories": list(stories)})

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
