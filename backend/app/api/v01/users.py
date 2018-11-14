# -*- coding: utf-8 -*-

from flask import jsonify
from flask_restful import Resource

from app import db
from pprint import pprint

# from app.decorators import auth

class ApiUsers(Resource):
    """
    http :5000/api/users
    http -F :5000/api/users/
    """
    endpoint_url = ["/users", "/users/<action>"]

    def get(self, action=None):
        # method = getattr(self, action, None)

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

        return jsonify({"msg": "test with mode <{action}>".format(action=action)})

    # @auth()
    # def privateFunction(self):
    #   pass
