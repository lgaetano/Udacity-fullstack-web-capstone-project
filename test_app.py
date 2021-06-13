import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from .database.models import setup_db, Patient, Provider

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # Bind app to current context
        with self.app.app.context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create tables
            self.db.create_all()

        self.patient = {
            "name": "Jahn Doe",
            "age": 48,
            "provider_id": 1,
        }

        self.provider = {
            "name": "Dr. Jekyll",
            "patients": [1, 2]
        }

        #TODO
        # Authentication tokens information
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        role_1 = self.auth["roles"]["Role 1"]["jwt_token"]
        role_2 = self.auth["roles"]["Role 2"]["jwt_token"]
        self.auth_headers = {
            "Role 1": f'Bearer {role_1}',
            "Role 2": f'Bearer {role_2}',
        }

    def tearDown(self):
        ''' Executed after each test run. '''
        pass

    '''
    Test GET Providers
    '''
    def test_get_providers(self):
        header_obj = {
            "Authorization": self.auth_headers["Role 1"]
        }
        res = self.client().get('/providers', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_get_provider_error(self):
        res = self.client().get('/providers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Unauthorized error.")

    '''
    Test GET Patients
    '''
    def test_get_patients(self):
        header_obj = {
            "Authorization": self.auth_headers["Role 1"]
        }
        res = self.client().get('/patients', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_patient_error(self):
        res = self.client().get('/patients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Unauthorized error.")

    '''
    Test POST Patients
    '''
    # def test_post_patients(self):

    '''
    Test PATCH Patients
    '''
    # def test_patch_patients(self):

    '''
    Test DELETE Patients
    '''
    # def test_delete_patients(self):

