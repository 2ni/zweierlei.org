# -*- coding: utf-8 -*-

from app import create_app
from app.config import test_config

from app.utils.dict import (filter_dict, diff_dict)

from redis import Redis

import unittest, json, subprocess, re, os, shutil, uuid

class Test(unittest.TestCase):
    """
    see setupModule or Suite for larger envs
    https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    """

    userdata = {"email": "test@zweierlei.org", "password": "test", "firstname": "Test"}
    userdata2 = {"email": "test2@zweierlei.org", "password": "test", "firstname": "Test2"}
    newuserdata = { "firstname": "John", "email": "newemail@zweierlei.org", "password": "12345", "anything": "shouldnotwork" }
    overwritedata = { "firstname": "Foo", "email": "foobar@zweierlei.org", "password": "54321" }
    storyid = "a96970f1-fbaa-439c-892a-cec49ea6376d"

    redis_process = None
    redis_port = None
    dir = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setUpClass(cls):
        """
        setting up custom redis instance for testing
        see https://www.reddit.com/r/Python/comments/2xspwx/how_to_set_up_a_test_environment_for_reddis_with/
        and https://security.openstack.org/guidelines/dg_avoid-shell-true.html
        """
        app = create_app(test_config)
        cls.app = app
        cls.client = app.test_client()

        cls.redis_port = re.sub("^.*?:(\d+).*$", r"\1", cls.app.config["REDIS_URL"])

        # safety check to avoid deleting prod
        if cls.redis_port == 6379:
            exit("about to delete data on redis prod!")

        cls.redis_process = subprocess.Popen(["redis-server", "--port", cls.redis_port])
        print("redis running on port {port}".format(port=cls.redis_port))

        # populate some testing data
        # os.system("cat redis-test.txt | redis-cli -p {port} 2>&1 >/dev/null".format(port=cls.redis_port))
        ps_cat = subprocess.Popen(["cat", "redis-test.txt"], stdout=subprocess.PIPE, shell=False)
        ps_redis = subprocess.Popen(["redis-cli", "-p", cls.redis_port], stdin=ps_cat.stdout, stdout=subprocess.PIPE, shell=False)
        ps_cat.stdout.close()
        ps_redis.communicate()
        ps_cat.wait()

    def setUp(self):
        print(self.sys_msg(self._testMethodName))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.app.config["UPLOAD_FOLDER"], ignore_errors=True)
        print("\nbye redis")
        # flush done while populating
        # os.system("echo 'FLUSHALL' | redis-cli --port {port}".format(port=cls.redis_port))
        cls.redis_process.terminate()
        cls.redis_process.wait()

    @staticmethod
    def sys_msg(msg, sep="*"):
        return "\n{sep} {msg}".format(sep="*"*20, msg=msg)

    def call(self, method, url, data={}, headers={}, content_type="application/json"):
        data = json.dumps(data) if content_type.find("json") != -1 else data
        resp = getattr(self.client, method)(url, data=data, content_type=content_type, headers=headers)
        return resp, json.loads(resp.get_data())

    def callWithToken(self, method, url, token, data={}, **kwargs):
        return self.call(method, url, data, headers = {"Authorization": "Bearer " + token}, **kwargs)


    def login(self, credentials=None):
        if not credentials:
            credentials = self.userdata
        resp, data = self.call("post", self.api("login"), credentials)
        return data

    def register(self, data):
        resp, newuser = self.call("post", self.api("register"), data)
        return resp.status_code, newuser


    @staticmethod
    def api(endpoint):
        if isinstance(endpoint, list):
            endpoint = "/".join(endpoint)

        return "/api/v01/" + endpoint


##### Tests start here #####

    def test_user_loginandrefreshtoken(self):
        data = self.login()

        self.assertEqual(data["msg"], "ok")
        self.assertTrue(data["access_token"])
        self.assertTrue(data["refresh_token"])
        self.assertEqual(data["firstname"], self.userdata["firstname"])

        resp, refresh = self.callWithToken("post", self.api("refresh"), data["access_token"])
        self.assertEqual(resp.status_code, 422)
        self.assertEqual(refresh["msg"], "Only refresh tokens are allowed")

        resp, refresh = self.callWithToken("post", self.api("refresh"), data["refresh_token"])
        self.assertEqual(data["msg"], "ok")
        assert "access_token" in refresh.keys()
        # print(resp.status_code, refresh)

    def test_user_getdata(self):
        tokens = self.login()

        resp, data = self.callWithToken("get", self.api("users"), tokens["access_token"])
        self.assertEqual(data["msg"], "ok")
        self.assertEqual(data["email"], self.userdata["email"])
        assert "uid" in data.keys()

        resp, data = self.callWithToken("get", self.api("users"), tokens["refresh_token"])
        self.assertEqual(resp.status_code, 422)
        assert "uid" not in data.keys()
        assert "email" not in data.keys()
        self.assertEqual(data["msg"], "Only access tokens are allowed")

    def test_user_getforeigndata(self):
        tokens = self.login()
        resp, data = self.callWithToken("get", self.api("users")+"/111", tokens["access_token"])
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(data["msg"], "not allowed")

    def test_user_register(self):
        # mandatory fields
        resp, data = self.call("post", self.api("register"), filter_dict(self.newuserdata, "email"))
        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data["msg"]["password"], "required element")

        # wrong email
        code, user = self.register({"email": "foobar", "password": "test"})
        self.assertEqual(code, 422)
        self.assertEqual(user["msg"]["email"], "wrong format")

        # register newuser
        code, newuser = self.register(self.newuserdata)
        self.assertEqual(newuser["msg"], "ok")
        self.assertEqual(newuser["email"], self.newuserdata["email"])
        assert "password" not in data.keys()

        # already registered
        code, data = self.register(self.newuserdata)
        self.assertEqual(code, 409)
        self.assertEqual(data["msg"]["email"], "exists")

    def test_user_update(self):
        # overwrite user data w/o or wrong token
        resp, data = self.call("post", self.api("users"), {"firstname": "John"})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data["msg"], "Missing Authorization Header")

        current = self.login()

        resp, data = self.callWithToken("post", self.api("users"), current["refresh_token"])
        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data["msg"], "Only access tokens are allowed")

        # overwrite user data w/o mandatory email
        resp, data = self.callWithToken("post", self.api("users"), current["access_token"], {"firstname": "John"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["msg"]["email"], "required element")

        current = self.login()
        # overwrite data
        resp, data = self.callWithToken("post", self.api("users"), current["access_token"], self.overwritedata)
        self.assertEqual(data["msg"], "ok")
        self.assertEqual(data["email"], self.overwritedata["email"])
        self.assertEqual(data["firstname"], self.overwritedata["firstname"])
        self.assertEqual(data["uid"], current["uid"])
        assert "password" not in data.keys()

        # ensure we can login with new creds
        newdata = self.login(self.overwritedata)
        assert "access_token" in newdata.keys()
        assert "refresh_token" in newdata.keys()
        self.assertEqual(newdata["uid"], data["uid"])
        self.assertEqual(newdata["email"], self.overwritedata["email"])

        # overwrite existing email
        resp, data = self.callWithToken("post", self.api("users"), current["access_token"], {"email": self.userdata2["email"]})
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(data["msg"]["email"], "exists")

    def test_story_getdata(self):
        resp, data = self.call("get", self.api(["stories", self.storyid]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["created_human"], "2017-12-24 17:30:00")
        self.assertEqual(diff_dict(data, "created,created_human,description,title,id,contenturl,lat,lon"), [])
        for k,v in {"lon": "8.5336", "lat": "47.3608", "created": "1514136600"}.items():
            self.assertEqual(data[k], v)

        resp, data = self.call("get", self.api(["stories", str(uuid.uuid4())]))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data["msg"], "not found")

    def test_story_getlatest(self):
        resp, stories = self.call("get", self.api("stories"))
        lastcreated = None
        assert len(stories) > 0
        assert len(stories) <= 3
        for story in stories:
            self.assertEqual(diff_dict(story, "created,created_human,description,title,id,contenturl,lat,lon"), [])
            if lastcreated:
                assert lastcreated >= story["created"]

            lastcreated = story["created"]

    def test_story_create(self):
        """
        new user, new story
        """
        code, user = self.register({"email": "storyteller@zweierlei.org", "password": "test"})

        # create story
        resp, data = self.callWithToken("post", self.api("stories"), user["access_token"], {"title": "Fancy thing", "description": "hahaha"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(diff_dict(data, "created,description,id,msg,title,created_human,contenturl"), [])

        # verify if returned contenturl matches our api url
        self.assertEqual(
            "{base}{apiurl}".format(
                base=self.app.config.get("BASE_URL"),
                apiurl=self.api(["stories", data["id"], "medias"])
            ),
            data["contenturl"])

        contenturl = data["contenturl"]
        storyurl =  self.api(["stories", data["id"]])

        # login needed
        resp, data = self.call("put", contenturl)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data["msg"], "Missing Authorization Header")

        # upload w/o image
        resp, data = self.callWithToken("put", contenturl, user["access_token"])
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data["msg"], "upload failed")

        # upload with gps image
        fns = []
        files = {
            "test-withgps.jpg": "id,lat,lon,created,created_human,relative_url",
            "test-withoutgps.jpg": "id,relative_url",
        }
        for name in files.keys():
            fns.append(open(os.path.join(self.dir, name), "rb"))

        resp, uploaded_medias = self.callWithToken("put", contenturl, user["access_token"], {"medias": fns}, content_type="multipart/form-data")

        self.assertEqual(resp.status_code, 200)

        # verify data from photo with gps data
        checks = {"created": "1540019730", "lat": "68.1547", "lon": "14.2112"}
        for tag, value in checks.items():
            self.assertEqual(uploaded_medias["medias"][0][tag], str(value))

        # check if files and thumbnails correctly saved and correct data
        for i, media in enumerate(uploaded_medias["medias"]):
            self.assertEqual(diff_dict(media, list(files.values())[i]), [])
            path = os.path.join(self.app.config.get("UPLOAD_FOLDER"), media["relative_url"])
            self.assertTrue(os.path.isfile(path))
            for size in self.app.config.get("UPLOAD_SIZES").keys():
                fn_thumb = media["relative_url"].replace(".orig.", ".{size}.".format(size=size))
                fn_path = os.path.join(self.app.config.get("UPLOAD_FOLDER"), media["relative_url"])
                self.assertTrue(os.path.isfile(fn_path))


        # after 1st media upload story should have created, lat, lon from that media
        resp, data = self.call("get", storyurl)
        self.assertEqual(data["created"], "1540019730")
        self.assertEqual(data["created_human"], "2018-10-20 07:15:30")

        # get media links from story
        resp, data = self.call("get", storyurl + "/medias")
        for i, media in enumerate(data["medias"]):
            self.assertEqual(media["id"], uploaded_medias["medias"][i]["id"])
            self.assertEqual(diff_dict(media, ["id", "url"]), [])

        # close files
        for fn in fns:
            fn.close()

    def test_story_wrong_media(self):
        resp, story = self.call("get", self.api(["stories", self.storyid]))
        apiurl = story["contenturl"]

        user = self.login()
        media = open(os.path.join(self.dir, "test-noimg.txt"), "rb")
        resp, data = self.callWithToken("put", apiurl, user["access_token"], {"medias": media}, content_type="multipart/form-data")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data["msg"], "upload failed")

    def test_story_upload_not_allowed(self):
        resp, story = self.call("get", self.api(["stories", self.storyid]))
        apiurl = story["contenturl"]

        code, user = self.register({"email": str(uuid.uuid4())+"@zweierlei.org", "password": "test"})
        media = open(os.path.join(self.dir, "test-withgps.jpg"), "rb")
        resp, data = self.callWithToken("put", apiurl, user["access_token"], {"medias": media}, content_type="multipart/form-data")
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(data["msg"], "not allowed")

    def test_story_upload_failed(self):
        """
        verify if uploaded files are deleted if writing to db fails
        see medias.py +80
        difficult to test, howto simulate failure of db writing?
        """
        pass


if __name__ == '__main__':
    unittest.main()
