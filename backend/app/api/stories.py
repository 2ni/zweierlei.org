# -*- coding: utf-8 -*-

from flask import jsonify
from flask_restful import Resource

from app import db

from datetime import datetime as dt

# from app.decorators import auth

class ApiStories(Resource):
    """
    http -F GET :5000/api/stories/e3dc859d-77de-49d1-b630-5e174f21ae92
    """
    endpoint_url = ["/stories", "/stories/<id>"]

    def get(self, id=None):
        # method = getattr(self, action, None)

        if id:
            story = db.hgetall("z:stories:{id}".format(id=id))
            return jsonify(story)
        else:
            # get latest stories
            latestIds = db.zrevrangebyscore("z:stories:index:created", "inf", 0, 0, 3)
            stories = []
            for id in latestIds:
                story = db.hgetall("z:stories:{id}".format(id=id))
                story["createdHuman"] = dt.utcfromtimestamp(int(story["created"])).strftime('%Y-%m-%d %H:%M:%S')

                stories.append(story)

            return jsonify(stories)

    # @auth()
    # def privateFunction(self):
    #   pass
