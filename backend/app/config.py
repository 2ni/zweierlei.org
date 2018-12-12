# -*- coding: utf-8 -*-

import os
from datetime import timedelta

class base_config(object):
    # use app.root_path!
    #BASEDIR = os.path.abspath(os.path.dirname(__file__))

    REDIS_URL = "redis://@localhost:6379/0"

    JWT_SECRET_KEY = "superduperPassw0rd"
    ACCESS_EXPIRES = timedelta(minutes=15)
    REFRESH_EXPIRES = timedelta(days=30)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # file uploads
    UPLOAD_FOLDER = os.path.join("static", "uploads")
    UPLOAD_DEPTH = 3

    DEBUG = False

class dev_config(base_config):
    DEBUG = True

class test_config(base_config):
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = os.path.join("static", "tests", "uploads")
    REDIS_URL = "redis://@localhost:6378/0"
