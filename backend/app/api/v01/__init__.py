# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

import glob, os, mmap, re, pkgutil

bp = Blueprint("api_v01", __name__)
api = Api(bp)
CORS(bp)

"""
from .users import ApiUsers
from .stories import ApiStories

api.add_resource(ApiUsers, *ApiUsers.endpoint_url, endpoint="users")
api.add_resource(ApiStories, *ApiStories.endpoint_url, endpoint="stories")
"""

# dynamically import api classes from current directory
curDir = os.path.dirname(os.path.realpath(__file__))
__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    module = modname.split(".")[-1] # eg users
    fn = os.path.join(curDir, module+".py") # eg users.py
    with open(fn, "rb", 0) as file, \
        mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        matches = re.findall(br'class ([^(]+)', s)
        for match in matches:
            classname = match.decode() # eg ApiUsers
            print("*** loading {module}/{classname}".format(module=module, classname=classname))
            classObject = __import__(modname, fromlist=[classname])
            obj = getattr(classObject, classname)()
            api.add_resource(obj, *obj.endpoint_url, endpoint="{module}/{classname}".format(module=module, classname=classname))
            continue
