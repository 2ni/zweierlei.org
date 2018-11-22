# -*- coding: utf-8 -*-

import os, sys, glob

from flask import redirect, Flask, g, request, Blueprint
from app import config
from app.extensions import (db, jwt)

from flask_restful import Api
from flask_cors import CORS

def create_app(config=config.base_config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    @app.before_request
    def clear_trailing_slash():
        rp = request.path
        if rp != '/' and rp.endswith('/'):
            return redirect(rp[:-1])

    register_blueprints(app)
    register_extensions(app)
    # register_converters(app)
    # register_errorhandlers(app)

    return app

def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_is_invalid(decrypted_token):
        jti = decrypted_token['jti']
        entry = db.get("z:tokens:{jti}".format(jti=jti))
        return True if entry is None else entry == "true"

def register_errorhandlers(app):
    pass

def register_converters(app):
    pass

def register_blueprints(app):
    from app.api.v01 import bp as apiV01Bp
    app.register_blueprint(apiV01Bp, url_prefix="/api/v0.1")

    """
    apiTest = Blueprint("apiTest", __name__)
    CORS(apiTest)
    api = Api(apiTest)

    from api.test import Test
    api.add_resource(Test, *Test.endpoint_url, endpoint="test")
    app.register_blueprint(apiTest, url_prefix="/<lang:lang_code>/api")
    """
