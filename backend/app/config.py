# -*- coding: utf-8 -*-

class base_config(object):
    # use app.root_path!
    #BASEDIR = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False

class dev_config(base_config):
    DEBUG = True

class test_config(base_config):
    DEBUG = True
