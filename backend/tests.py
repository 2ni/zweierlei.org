# -*- coding: utf-8 -*-

from app import create_app
from app.config import test_config

from app.utils.dict import (filter_dict)

from redis import Redis

import unittest, json, subprocess, re

class Test(unittest.TestCase):
    userdata = {"email": "test@zweierlei.org", "password": "test", "firstname": "Test"}
    userdata2 = {"email": "test2@zweierlei.org", "password": "test", "firstname": "Test2"}
    newuserdata = { "firstname": "John", "email": "newemail@zweierlei.org", "password": "12345", "anything": "shouldnotwork" }
    overwritedata = { "firstname": "Foo", "email": "foobar@zweierlei.org", "password": "54321" }
    redis_process = None
    redis_port = None

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
        print("\nbye redis")
        # flush done while populating
        # os.system("echo 'FLUSHALL' | redis-cli --port {port}".format(port=cls.redis_port))
        cls.redis_process.terminate()
        cls.redis_process.wait()

    @staticmethod
    def sys_msg(msg, sep="*"):
        return "\n{sep} {msg}".format(sep="*"*20, msg=msg)

    def call(self, method, url, data={}, headers={}):
        resp = getattr(self.client, method)(url, data=json.dumps(data), content_type="application/json", headers=headers)
        return resp, json.loads(resp.get_data())

    def callWithToken(self, method, url, token, data={}):
        return self.call(method, url, data, headers = {"Authorization": "Bearer " + token})


    def login(self, credentials=None):
        if not credentials:
            credentials = self.userdata
        resp, data = self.call("post", self.api("login"), credentials)
        return data

    def register(self, data):
        resp, newuser = self.call("post", self.api("register"), data)
        return newuser


    @staticmethod
    def api(endpoint):
        return "/api/v0.1/" + endpoint


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

    def test_user_register(self):
        # mandatory fields
        resp, data = self.call("post", self.api("register"), filter_dict(self.newuserdata, "email"))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["msg"]["password"], "required element")

        # register newuser
        resp, newuser = self.call("post", self.api("register"), self.newuserdata)
        self.assertEqual(newuser["msg"], "ok")
        self.assertEqual(newuser["email"], self.newuserdata["email"])
        assert "password" not in data.keys()

        # already registered
        resp, data = self.call("post", self.api("register"), self.newuserdata)
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(data["msg"], "email already registered")

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
        self.assertEqual(data["msg"], "email already registered")


if __name__ == '__main__':
    unittest.main()
