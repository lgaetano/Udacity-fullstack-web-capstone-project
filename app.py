# import os
# from _typeshed import NoneType
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Provider, Patient
# from auth import AuthError, requires_auth
import json

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)

  #CORS Headers
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def index():
    return jsonify({
      'message': 'Capstone Project'
    })

  @app.route('/patients', methods=['GET'])
  # @requires_auth('get:patients')
  def get_patients(token):
    ''' Retrieve all patients. '''

    try:
      #Get all patients
      patient_detail = list(map(Patient.format, Patient.query.all()))
      
      return jsonify({
        "success": True,
        "patients": patient_detail,
        "total_patients": len(Patient.query.all()),
      }), 200

    except Exception:
      abort(404)
          
  @app.route('/patients', methods=['POST'])
  # @requires_auth('post:patients')
  def add_patient(token):
    ''' Create new patient record. '''
    
    # Get data from body
    data = request.get_json()

    # If no data, abort
    if data is None:
      abort(400, "No data provided")

    name = data.get("name", None)
    age = data.get("age", None)
    provider_id = data.get("provider_id", NoneType)

    # If no name supplied, abort
    if not name:
        abort(422, "No name provided")
    # If no age supplied, abort
    if not age:
        abort(422, "No age provided")
    # If no provider_id supplied, abort
    if not provider_id:
        abort(422, "No provider_id provided")

    try:
      #Create new patient record
      patient = Patient(
        name=name, 
        age=age, 
        provider_id=provider_id)
      #Insert new patient record
      patient.insert()

    except Exception:
      abort(400)
    
    return jsonify({
      "success": True
    }), 200

  @app.route('/providers', methods=['GET'])
  # @requires_auth('get:providers')
  def get_providers(token):
    ''' Retrieve all providers. '''

    try:
      #Get all providers
      provider_detail = list(map(Provider.format, Provider.query.all()))
      
      return jsonify({
        "success": True,
        "patients": provider_detail,
        "total_providers": len(Provider.query.all()),
      }), 200

    except Exception:
      abort(404)
          
  @app.route('/providers', methods=['POST'])
  # @requires_auth('post:providers')
  def add_provider(token):
    ''' Create new provider record. '''
    
    # Get data from body
    data = request.get_json()

    # If no data, abort
    if data is None:
      abort(400, "No data provided")

    name = data.get("name", None)
    ##TODO: HOW TO ADD PATIENTS
    # patients = data.get("provider_id", NoneType)

    # If no name supplied, abort
    if not name:
        abort(422, "No name provided")
    ##TODO
    # # If no patient supplied, abort
    # if not provider_id:
    #     abort(422, "No provider_id provided")

    try:
      #Create new provider record
      provider = Provider(
        name=name,
        # patients=provider_id
        )
      #Insert new patient record
      provider.insert()

    except Exception:
      abort(400)
    
    return jsonify({
      "success": True
    }), 200

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)