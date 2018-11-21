# -*- coding: utf-8 -*-

def filter_dict(someDict, keys):
    """
    return only given <keys> from a dict someDict
    """
    return { k: someDict[k] for k in keys if k in someDict }

def merge_dict(*args):
    ret = {}
    for d in args:
        ret = {**ret, **d}

    return ret
