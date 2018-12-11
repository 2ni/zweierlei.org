# -*- coding: utf-8 -*-

from flask import jsonify, make_response
from flask_restful import Resource

class ZweierleiResource(Resource):

    def response(self, type, field=None):
        respErrs = {
            "wrong creds": make_response(jsonify({"msg": "bad email/password"}), 401),
            "email exists": make_response(jsonify({"msg": "email already registered"}), 409),
            "not allowed": make_response(jsonify({"msg": "not allowed"}), 403),
            "not found": make_response(jsonify({"msg": "entry does not exist"}), 404),
            "not implemented": make_response(jsonify({"msg": "function ist not (yet) implemented"}), 501),
            "generic": make_response(jsonify({"msg": "an error occured"}), 400)
        }
        if field:
            respErrs["missing"] = make_response(jsonify({"msg": "{field} is missing".format(field=field)}), 422);

        return respErrs[type] if type in respErrs else respErrs["generic"]
