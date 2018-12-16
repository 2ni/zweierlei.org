# -*- coding: utf-8 -*-

import os
from datetime import timedelta

class base_config(object):
    # use app.root_path!
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    BASEURL = "https://zweierlei.org"
    UPLOADURL = "{base}/uploads".format(base=BASEURL)

    REDIS_URL = "redis://@localhost:6379/0"

    JWT_SECRET_KEY = "superduperPassw0rd"
    ACCESS_EXPIRES = timedelta(minutes=15)
    REFRESH_EXPIRES = timedelta(days=30)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # file uploads
    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "uploads")
    UPLOAD_DEPTH = 3

    DEBUG = False

class dev_config(base_config):
    BASEURL = "http://127.0.0.1:5000"
    UPLOADURL = "{base}/uploads".format(base=BASEURL)
    DEBUG = True

class test_config(base_config):
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    BASEURL = "http://127.0.0.1:5000"
    UPLOADURL = "{base}/uploads".format(base=BASEURL)

    DEBUG = True
    TESTING = True
    os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "tests", "uploads")
    REDIS_URL = "redis://@localhost:6378/0"
