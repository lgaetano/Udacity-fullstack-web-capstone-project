
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Patient, Provider

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}".format(self.database_name)
        setup_db(self.app, self.database_path)


        self.patient = {
            "name": "Jahn Doe",
            "age": 48,
            "provider_id": 1,
        }

        self.provider = {
            "name": "Dr. Jekyll",
            "patients": [1, 2]
        }

    def tearDown(self):
        ''' Executed after each test run. '''
        pass

    def test_get_providers(self):
        header_obj = {
            "Authorization": self.auth_headers["INSERT "]
        }