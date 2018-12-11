# -*- coding: utf-8 -*-

import os
from flask import current_app

def uuid2dir(uuid):
    base_dir = current_app.config.get("UPLOAD_FOLDER")
    return os.path.join(base_dir, *list(uuid.replace("-", ""))[0:current_app.config.get("UPLOAD_DEPTH")])
