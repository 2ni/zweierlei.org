# -*- coding: utf-8 -*-

import uuid, json, os, re

from flask import jsonify, request, url_for, current_app
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from werkzeug.utils import secure_filename

from app import db
from app.models.photoupload import Photoupload
from app.api.zweierleiresource import ZweierleiResource
from app.utils.dir import mediaid2url

from datetime import datetime as dt

from app.decorators import jwt_required_consume_attach

class ApiMedias(ZweierleiResource):
    """
    http -F GET :5000/api/v01/stories/a96970f1-fbaa-439c-892a-cec49ea6376d/medias
    """
    endpoint_url = ["/stories/<id>/medias"]

    def get(self, id):
        """
        get all medias from a story
        """
        data = db.lrange("z:mediasByStory:{id}".format(id=id), 0, -1)

        medias = []
        for relative in data:
            url = mediaid2url(relative)
            medias.append({
                "id": re.sub("^.*/([^.]*).*", r"\1", relative),
                "url": url,
            })

        return jsonify({"msg": "ok", "medias": medias})

    @jwt_required_consume_attach
    def put(self, id):
        """
        Add media to stories
        see https://stackoverflow.com/questions/28982974/flask-restful-upload-image

        http -f -F PUT :5000/api/v01/stories/a96970f1-fbaa-439c-892a-cec49ea6376d/medias Authorization:"Bearer <jwt>" medias@<file> medias@<file>...
        """

        media_uploads = request.files.getlist("medias")
        uid = get_jwt_identity()

        if not id:
            return self.response("required", "id")

        # prechecks to avoid uploading if not ready
        # these checks are also done when updating db below

        # story must exist (precheck not done atomically)
        if not db.exists("z:stories:{id}".format(id=id)):
            return self.response("not found")

        # story must belong to user (precheck not done atomically)
        if db.zscore("z:storiesByUser:{uid}".format(uid=uid), id) == None:
            return self.response("not allowed")

        # upload data physically
        medias = []
        for i, media in enumerate(media_uploads):
            with Photoupload(media) as photoupload:
                data = photoupload.save()

                verify = isinstance(data, dict) and data.get("msg")
                if verify == "ok":
                    del data["msg"]
                    data["url"] = mediaid2url(data["relative_url"])
                    medias.append(data)

        if not medias:
            return self.response("upload failed")

        # update database if fails, medias are deleted
        ret = db.appendMediasToStory(args=["uid", uid, "id", id, "medias", json.dumps(medias)]).lower()
        if ret == "ok":
            # TODO generate smaller files in task queue (flask-rq2)
            return jsonify({"msg": "ok", "medias": medias})
        else:
            for media in medias:
                file = os.path.join(current_app.config.get("UPLOAD_FOLDER"), media["url"])
                os.remove(file)

            return self.response(ret)

        # TODO use url_for("uploaded_file", filename="foo"))
        # mediakeys = [list(k.keys())[0] for k in medias]
        # mediakeys = [v["id"] for v in medias]

