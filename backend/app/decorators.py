# -*- coding: utf-8 -*-

from functools import wraps
from flask_jwt_extended import (verify_jwt_in_request)

from flask import request

def jwt_required_consume_attach(fn):
    """
    do the same as jwt_required
    but avoid broken pipe error / ConnectionError
    due to attachements
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.files:
            for k,v in request.files.to_dict().items():
                data = request.files.getlist(k)
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper
