# -*- coding: utf-8 -*-

import os, re
from flask import current_app

def uuid2dir(uuid):
    """
    eg uuid 87f0865f-7547-4402-bf84-582ff5655097.jpeg
    returns 8/7/f/87f0865f-7547-4402-bf84-582ff5655097.jpeg
    """
    return os.path.join(*list(uuid.replace("-", ""))[0:current_app.config.get("UPLOAD_DEPTH")])

def mediaid2url(idending):
    """
    idending eg 8/7/f/87f0865f-7547-4402-bf84-582ff5655097.jpeg
    it's the "id" saved in the db
    returns eg https://zweierlei.org/uploads/8/7/f/87f0865f-7547-4402-bf84-582ff5655097.orig.jpeg
    """
    id, ending = re.findall(r"^(.*)\.([^.]*)$", idending)[0] # 8/7/f/87f0865f-7547-4402-bf84-582ff5655097.orig.jpeg
    baseurl = current_app.config.get("UPLOAD_URL")
    return "{baseurl}/{id}.{ending}".format(baseurl=baseurl, id=id, ending=ending)
