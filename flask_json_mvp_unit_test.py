from flask import Flask
from app import app
import unittest
import tempfile
import json

class ModUnitTest(unittest.TestCase):

    json_headers = {'Content-type': 'application/json'}

    def lf(self, file):
        path = "unit_test/data/%s" %(file)
        json_data = None

        with open(path) as json_file:
            json_data = json.load(json_file)

            return json_data

    def runTest(self):
        pass

    def create_app(self):
        print "create_app"
        app = Flask(__name__)

        return app

    def setUp(self):
        print "setUp"
        self.client = app.test_client()
        self.client.testing = True
        pass

    def tearDown(self):
        print "tearDown"
        pass

    def test_mod_json(self):
        print "test_mod_json"

        json_data = self.lf("organization.json")
        response = self.client.post("/organization", data = json.dumps(json_data),
                                    follow_redirects=True, headers =
                                    self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Add Test Record"


if __name__ == "__main__":
    unittest.main()
