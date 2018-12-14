# -*- coding: utf-8 -*-

from flask import jsonify, request
from app.api.zweierleiresource import ZweierleiResource

import re

# from app.decorators import auth

class ApiTest(ZweierleiResource):
    """
    Playground api
    http post :5000/api/v01/foo
    """
    endpoint_url = ["/foo/mario", "/bar"]

    def post(self):
        endpointUsed = [u for u in self.endpoint_url if u in request.path][0]
        # endpointUsed = re.sub("^.*?([^/]*)$", r"\1", request.path)
        resp =  jsonify({"msg": "ok", "endpoint": endpointUsed})
        resp.status_code = 201
        return resp
