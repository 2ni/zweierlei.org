# -*- coding: utf-8 -*-

def filter_dict(someDict, keys):
    """
    return only given <keys> from a dict someDict
    """
    if not isinstance(keys, list):
        keys = keys.replace(" ", "").split(",")

    return { k: someDict[k] for k in keys if k in someDict }

def exclude_dict(someDict, keys):
    """
    return dict by excluding given keys
    """
    if not isinstance(keys, list):
        keys = [keys]

    return {k: someDict[k] for k in someDict if k not in keys}

def merge_dict(*args):
    ret = {}
    for d in args:
        ret = {**ret, **d}

    return ret


def check_mandatory_fields(data, mandatory):
        # mandatory fields
        if not isinstance(mandatory, list):
            mandatory = [mandatory]

        err = {}
        for elm in mandatory:
            if (elm not in data):
                err[elm] = "required element"

        if err:
            return {"msg": err}

        return err

def dict2list(some_dict):
    """
    convert a flat dict to a list of [key, value, key, value, ...]
    to be used for redis lua commands
    """
    some_list = []
    for k,v in some_dict.items():
        some_list.append(k)
        some_list.append(v)

    return some_list

def diff_dict(some_dict, keys):
    """
    compare a some_dict with mandatory keys
    missing have -
    too many have +
    """
    if not isinstance(keys, list):
        keys = keys.replace(" ", "").split(",")

    return ["+"+k for k in some_dict if k not in keys] + ["-"+k for k in keys if k not in some_dict]
