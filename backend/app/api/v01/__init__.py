# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

bp = Blueprint("api_v01", __name__)
api = Api(bp)

from .users import ApiUsers
from .stories import ApiStories

api.add_resource(ApiUsers, *ApiUsers.endpoint_url, endpoint="users")
api.add_resource(ApiStories, *ApiStories.endpoint_url, endpoint="stories")
