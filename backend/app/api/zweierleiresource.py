# -*- coding: utf-8 -*-

from flask import jsonify, make_response
from flask_restful import Resource

class ZweierleiResource(Resource):

    def response(self, type):
        respErrs = {
            "wrong creds": make_response(jsonify({"msg": "bad email/password"}), 401),
            "email exists": make_response(jsonify({"msg": "email already registered"}), 409),
            "uid missing": make_response(jsonify({"msg": "uid is missing"}), 422),
            "not allowed": make_response(jsonify({"msg": "not allowed"}), 403),
            "generic": make_response(jsonify({"msg": "an error occured"}), 400)
        }
        return respErrs[type] if type in respErrs else respErrs["generic"]
