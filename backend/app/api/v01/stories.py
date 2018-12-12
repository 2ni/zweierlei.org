# -*- coding: utf-8 -*-

import uuid, json

from flask import jsonify, request, url_for
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from werkzeug.utils import secure_filename

from app import db
from app.models.photoupload import Photoupload
from app.api.zweierleiresource import ZweierleiResource
from app.utils.dict import (check_mandatory_fields, filter_dict, dict2list, merge_dict)

from datetime import datetime as dt

from app.decorators import jwt_required_consume_attach

class ApiStories(ZweierleiResource):
    """
    http -F GET :5000/api/v0.1/stories/e3dc859d-77de-49d1-b630-5e174f21ae92
    """
    endpoint_url = ["/stories", "/stories/<id>"]
    exposed_fields = ["title", "description"]

    def get(self, id=None):
        # method = getattr(self, action, None)

        if id:
            story = db.hgetall("z:stories:{id}".format(id=id))
            if story:
                created = str(round(db.zscore("z:stories:index:created", id)))
                story["id"] = id
                story["url"] = "tbd" # TODO
                story["created"] = created
                story["created_human"] = dt.utcfromtimestamp(int(story["created"])).strftime('%Y-%m-%d %H:%M:%S')
                return jsonify(story)
            else:
                return self.response("not found")
        else:
            # get latest stories
            # zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=<type 'float'>)
            latestIds = db.zrevrangebyscore("z:stories:index:created", "inf", 0, 0, 3, True)
            stories = []
            for (id, created) in latestIds:
                story = db.hgetall("z:stories:{id}".format(id=id))
                story["id"] = id
                story["url"] = "tbd" # TODO
                story["created"] = created
                story["created_human"] = dt.utcfromtimestamp(int(story["created"])).strftime('%Y-%m-%d %H:%M:%S')

                stories.append(story)

            return jsonify(stories)

    @jwt_required_consume_attach
    def put(self, id=None):
        """
        Add media to stories
        see https://stackoverflow.com/questions/28982974/flask-restful-upload-image

        http -f -F PUT :5000/api/v0.1/stories/a96970f1-fbaa-439c-892a-cec49ea6376d Authorization:"Bearer <jwt>" medias@<file> medias@<file>...
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
                if data:
                    medias.append(data)

        if not medias:
            return self.response("nothing to do")

        # update database if fails, medias are deleted
        ret = db.appendMediasToStory(args=["uid", uid, "id", id, "medias", json.dumps(medias)]).lower()
        print(ret)
        if ret == "ok":
            return jsonify({"msg": "ok", "medias": medias})
        else:
            # TODO delete uploaded medias
            print(ret)
            return self.response(ret)

        # TODO use url_for("uploaded_file", filename="foo"))
        # mediakeys = [list(k.keys())[0] for k in medias]
        # mediakeys = [v["id"] for v in medias]

    @jwt_required
    def post(self, id=None):
        """
        Create or Update  entry
        Entry will be replaced, all values must be given

        http -F POST :5000/api/v0.1/stories/a96970f1-fbaa-439c-892a-cec49ea6376d Authorization:"Bearer <jwt>"  title=...
        """
        rawData = request.json or {}
        dataToSave = filter_dict(rawData, self.exposed_fields)
        dataToSave["uid"] = get_jwt_identity()
        if not id:
            now = dt.utcnow()
            dataToSave["id"] = str(uuid.uuid4())
            dataToSave["created"] = now.strftime("%s") # add created time of now. Will be updated by media upload
            dataToSave["created_human"] = now.strftime('%Y-%m-%d %H:%M:%S')
        else:
            dataToSave["id"] = id

        ret = db.replaceOrInsertStory(args=dict2list(dataToSave)).lower()
        del dataToSave["uid"] # do not return user uid
        if ret == "ok":
            return jsonify(merge_dict(dataToSave, {"msg": "ok"}))
        else:
            # eg "required element:uid,description" -> call as "required element", "uid,description"
            return self.response(*ret.split(":"))

    @jwt_required
    def delete(self, id):
        """
        http -F -f DELETE :5000/api/v0.1/stories/a96970f1-fbaa-439c-892a-cec49ea6376d
        """
        return self.response("not implemented")
