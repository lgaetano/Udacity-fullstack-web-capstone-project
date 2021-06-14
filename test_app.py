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

        self.new_patient = {
            "name": "Jahn Doe",
            "age": 48,
            "provider_id": 1
        }

        self.new_provider = {
            "name": "Dr. Jekyll",
            "patients": [1, 2]
        }

        # Set up authentication tokens
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        ins_agent_jwt = self.auth["roles"]["Insurance Agent"]["jwt_token"]
        ins_manager_jwt = self.auth["roles"]["Insurance Manager"]["jwt_token"]
        self.auth_headers = {
            "Insurance Agent": f'Bearer {ins_agent_jwt}',
            "Insurance Manager": f'Bearer {ins_manager_jwt}'
        }

        # Bind app to current context
        with self.app.app.context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create tables
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test run. '''
        pass

    '''
    Test GET Providers
    '''
    def test_get_providers(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Agent"]
            }
        res = self.client().get('/providers', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_401_get_provider_error(self):
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
            "Authorization": self.auth_headers["Insurance Agent"]
        }

        res = self.client().get('/patients', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_401_get_patient_error(self):
        res = self.client().get('/patients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Unauthorized error.")

    '''
    Test POST Patients
    '''
    def test_create_new_patient(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Agent"]
        }

        res = self.client().post('/patients', 
                                json=self.new_patient, 
                                headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_401_create_new_patient(self):
        res = self.client().post('/patients', json=self.new_patient)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unauthorized Error")

    '''
    Test PATCH Patients
    '''
    def test_patch_patients(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Manager"]
        }

        # Add entry to database
        self.client().post('/patients', json=self.new_patient,
                           headers=header_obj)

        res = self.client().patch(
            'patients/2', json={'age': 342},
            headers=header_obj
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_patch_patients(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Manager"]
        }

        res = self.client().patch(
            'patients/200', json={'age': 342},
            headers=header_obj
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource Not Found")

    '''
    Test DELETE Patients
    '''
    def test_delete_patients(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Manager"]
        }
        
        # Add entry to database
        self.client().post('/patients', json=self.new_patient,
                           headers=header_obj)

        res = self.client().delete('/patients/3', 
                                headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_delete_patients(self):
        header_obj = {
            "Authorization": self.auth_headers["Insurance Manager"]
        }

        res = self.client().delete('/patients/42', 
                                headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Resource Not Found")