# -*- coding: utf-8 -*-

import uuid, json, os, re

from flask import jsonify, request, url_for, current_app
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from werkzeug.utils import secure_filename

from app import db
from app.api.zweierleiresource import ZweierleiResource
from app.utils.dict import (check_mandatory_fields, filter_dict, dict2list, merge_dict)

from datetime import datetime as dt

from app.decorators import jwt_required_consume_attach

class ApiStories(ZweierleiResource):
    """
    http -F GET :5000/api/v01/stories/e3dc859d-77de-49d1-b630-5e174f21ae92
    http -F GET :5000/api/v01/stories
    """
    endpoint_url = ["/stories", "/stories/<id>"]
    exposed_fields = ["title", "description", "activity"]

    def get(self, id=None):
        if id:
            story = ApiStories._get_story(id)
            if story:
                return jsonify(story)
            else:
                return self.response("not found")
        else:
            # get latest stories
            # zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=<type 'float'>)
            latestIds = db.zrevrangebyscore("z:stories:index:created", "inf", 0, 0, current_app.config.get("NUM_STORIES"), True)
            stories = []
            for (id, created) in latestIds:
                story = ApiStories._get_story(id, created)
                if story:
                    stories.append(story)

            if stories:
                return jsonify(stories)
            else:
                return self.resonse("not found")


    @jwt_required
    def post(self, id=None):
        """
        Create or Update  entry
        Entry will be replaced, all values must be given

        http -F POST :5000/api/v01/stories/a96970f1-fbaa-439c-892a-cec49ea6376d Authorization:"Bearer <jwt>"  title=...
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
            return jsonify(merge_dict(dataToSave, {
                "msg": "ok",
                "content_url": ApiStories._get_content_url(dataToSave["id"])
            }))
        else:
            # eg "required element:uid,description" -> call as "required element", "uid,description"
            return self.response(*ret.split(":"))

    @jwt_required
    def delete(self, id):
        """
        http -F -f DELETE :5000/api/v01/stories/a96970f1-fbaa-439c-892a-cec49ea6376d
        """
        return self.response("not implemented")

    @staticmethod
    def _get_content_url(id):
        """
        get content url to upload media to
        """
        curdir = os.path.dirname(os.path.realpath(__file__))
        apiurl = re.sub("^.*(/api.*)", r"\1", curdir)
        baseurl = current_app.config.get("BASE_URL")

        return "{baseurl}{apiurl}/stories/{id}/medias".format(
            baseurl=baseurl,
            apiurl=apiurl,
            id=id
        )

    @staticmethod
    def _get_story(id, created=None):
        """
        get all necessary data for a story from db
        """
        story = db.hgetall("z:stories:{id}".format(id=id))
        if not story:
            return None

        if not created:
            createdvalue = db.zscore("z:stories:index:created", id)
            created = str(round(createdvalue)) if createdvalue else None

        story["id"] = id
        story["created"] = created
        story["created_human"] = dt.utcfromtimestamp(int(story["created"])).strftime('%Y-%m-%d %H:%M:%S')
        story["content_url"] = ApiStories._get_content_url(id)

        location = db.geopos("z:stories:position", id)[0]
        if location:
            story["lon"] = str(round(location[0], 4))
            story["lat"] = str(round(location[1], 4))

        return story
