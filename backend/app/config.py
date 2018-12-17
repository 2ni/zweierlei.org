# -*- coding: utf-8 -*-

import os
from datetime import timedelta

class base_config(object):
    # use app.root_path!
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    BASE_URL = "https://zweierlei.org"
    UPLOAD_URL = "{base}/uploads".format(base=BASE_URL)
    UPLOAD_SIZES = {"s": 180, "m": 360, "l": 720, "xl": 1440}

    REDIS_URL = "redis://@localhost:6379/0"

    JWT_SECRET_KEY = "superduperPassw0rd"
    ACCESS_EXPIRES = timedelta(minutes=15)
    REFRESH_EXPIRES = timedelta(days=30)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # file uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    UPLOAD_DEPTH = 3

    DEBUG = False

class dev_config(base_config):
    BASE_URL = "http://127.0.0.1:5000"
    UPLOAD_URL = "{base}/uploads".format(base=BASE_URL)
    DEBUG = True

class test_config(base_config):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    BASE_URL = "http://127.0.0.1:5000"
    UPLOAD_URL = "{base}/uploads".format(base=BASE_URL)

    DEBUG = True
    TESTING = True
    os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "tests", "uploads")
    REDIS_URL = "redis://@localhost:6378/0"
