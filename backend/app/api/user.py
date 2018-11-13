# -*- coding: utf-8 -*-

from flask import jsonify
from flask_restful import Resource

# from app.decorators import auth

class ApiUser(Resource):
    """
    http :5000/api/user
    http -F :5000/api/user/
    """
    endpoint_url = ["/user", "/user/<action>"]

    def get(self, action=None):
        # method = getattr(self, action, None)

        return jsonify({"msg": "test with mode <{action}>".format(action=action)})

    # @auth()
    # def privateFunction(self):
    #   pass
