# -*- coding: utf-8 -*-

import os, sys, glob

from flask import redirect, Flask, g, request, Blueprint
from app import config
from app.extensions import (db)

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

def register_errorhandlers(app):
    pass

def register_converters(app):
    pass

def register_blueprints(app):
    from app.api.users import ApiUsers
    bp = Blueprint("apiUsers", __name__)
    CORS(bp)
    api = Api(bp)
    api.add_resource(ApiUsers, *ApiUsers.endpoint_url, endpoint="users")
    app.register_blueprint(bp, url_prefix="/api")

    from app.api.stories import ApiStories
    bp = Blueprint("apiStories", __name__)
    api = Api(bp)
    api.add_resource(ApiStories, *ApiStories.endpoint_url, endpoint="stories")
    app.register_blueprint(bp, url_prefix="/api")

    """
    apiTest = Blueprint("apiTest", __name__)
    CORS(apiTest)
    api = Api(apiTest)

    from api.test import Test
    api.add_resource(Test, *Test.endpoint_url, endpoint="test")
    app.register_blueprint(apiTest, url_prefix="/<lang:lang_code>/api")
    """
