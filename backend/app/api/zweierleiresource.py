# -*- coding: utf-8 -*-

from flask import jsonify, make_response
from flask_restful import Resource

class ZweierleiResource(Resource):
    patterns = {
        "wrong creds": 401,
        "exists": 409,
        "not allowed": 403,
        "not found": 404,
        "not implemented": 501,
        "generic": 400,
        "required": 422,
        "failed": 404,
    }

    def response(self, type, fields=None):
        """
        call examples:
            response("required element:uid,description")
            response("already registered", "email")
            response("not allowed")
            response("required element", ["id", "uid"])
        """
        status_code = 400

        for pattern, code in self.patterns.items():
            if type.find(pattern) != -1:
                status_code = code
                break

        if fields:
            fields = fields.split(",")

            msg = {}
            for field in fields:
                msg[field] = type
        else:
            msg = type

        return make_response(jsonify({"msg": msg}), status_code)
