# -*- coding: utf-8 -*-

class base_config(object):
    # use app.root_path!
    #BASEDIR = os.path.abspath(os.path.dirname(__file__))

    REDIS_URL = "redis://@localhost:6379/0"

    JWT_SECRET_KEY = "superduperPassw0rd"

    DEBUG = False

class dev_config(base_config):
    DEBUG = True

class test_config(base_config):
    DEBUG = True
