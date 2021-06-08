import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Provider, Patient
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/patients', methods=['GET'])
  @requires_auth('get:patients')
  def get_patients(token):
    ''' Retrieve Patients. '''
    try:
      patient_detail = list(map(Patient.format, Actor.query.all()))
      return jsonify({
        "success": True,
        "actors": patient_detail,
        "total_patients": len(Patient.query.all()),
      }) 200

    except Exception:
      abort(404)
          
  @app.route('/coolkids')
  def be_cool():
      return "Be cool, man, be coooool! You're almost a FSND grad!"

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)