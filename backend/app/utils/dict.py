# -*- coding: utf-8 -*-

def filter_dict(someDict, keys):
    """
    return only given <keys> from a dict someDict
    """
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
