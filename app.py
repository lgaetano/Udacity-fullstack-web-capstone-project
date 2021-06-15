from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from database.models import setup_db, Provider, Patient
from auth.auth import AuthError, requires_auth

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
  @requires_auth('get:patients')
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

  @app.route('/providers', methods=['GET'])
  @requires_auth('get:providers')
  def get_providers(token):
    ''' Retrieve all providers. '''

    try:
      #Get all providers
      provider_detail = list(map(Provider.format, Provider.query.all()))
      
      return jsonify({
        "success": True,
        "providers": provider_detail,
        "total_providers": len(Provider.query.all()),
      }), 200

    except Exception:
      abort(404)
          
  @app.route('/patients', methods=['POST'])
  @requires_auth('post:patients')
  def add_patient(token):
    ''' Create new patient record. '''
    
    # Get data from body
    data = request.get_json()

    # If no data, abort
    if data is None:
      abort(400, "No data provided")

    # Retrieve data for new record
    name = data.get("name", None)
    age = data.get("age", None)
    provider_id = data.get("provider_id", None)

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

  @app.route('/patients/<int:id>', methods=['PATCH'])
  @requires_auth('patch:patients')
  def update_patient(token, id):
    ''' Update patient record. '''
    
    # Query for record
    patient = Patient.query.filter(Patient.id == id).one_or_none()

    # If no data, abort
    if patient is None:
      abort(404, "No patient with this id found.")

    try:
      # Get data from body
      data = request.get_json()

      # If no data, abort
      if data is None:
        abort(400, "No data provided")

      # Retrieve data to update  record
      name = data.get("name", None)
      age = data.get("age", None)
      provider_id = data.get("provider_id", None)

      # Insert updated data
      patient.name = name
      patient.age = age
      patient.provider_id = provider_id

      # Update patient record
      patient.update()

    except Exception:
      abort(422, "Updated failed.")
    
    return jsonify({
      "success": True
    }), 200
          
  @app.route('/patients/<int:id>', methods=['DELETE'])
  @requires_auth('delete:patients')
  def delete_patient(token, id):
    ''' Delete individual patient. '''

    patient = Patient.query.filter(Patient.id == id).one_or_none()

    # If no patient matches, abort
    if Patient is None:
      abort(404, "No patient with id " + str(id) + " found.")
    try:
      #Delete patient record
      patient.delete()
             
      return jsonify({
        "success": True,
        "deleted": id,
      }), 200

    except Exception:
      abort(404)

  return app

app = create_app()

# Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }),  500

@app.errorhandler(AuthError)
def authentication_failed(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['code']
    }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)