# Udacity Full Stack Insurance Agency Capstone Specifications API Backend

## About
The Insurance Agency models a compan that is responsible for managing patient and provider relationships. The app is used to assign patients to providers.

The insurance agency has an Insurance Agent role who can retrieve and add new patient records and an Insurance Manager role that has all permissions, including updating and deleting patient records.


The endpoints and request specifications for these endpoints are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or Postman since there is no frontend for the app at this time.

## Getting Started

### Installing Dependencies

### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies
Run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server
From within the root directory, ensure you are working using your created virtual environment.

To run the server, execute:
```
python3 app.py
or 
FLASK_APP=app.py flask run
```
We can now also open the application via Heroku using the URL:
https://TODO


## API DOCUMENTATION
### Endpoint Library

#### base URL:
https://TODO


#### GET '/patients'
Returns a list of all available patients, patient detail, total number of patients and a success value.
Returns via Postman:
{
    "patients": [
        {
            "id": 1,
            "name": "Carol",
            "age": 15,
            "provider_id": 3
        },
        {
            "id": 2,
            "name": "Ethel",
            "age": 25,
            "provider_id": 2
        },
        {
            "id": 3,
            "name": "Sheila",
            "age": 45,
            "provider_id": 2
        }
    ],
    "success": True,
    "total_patients": 3
}

#### GET '/providers'
Returns a list of all available providers, provider detail, total number of providers and a success value.
Returns via Postman:
{
    "providers": [
        {
            "id": 2,
            "name": "Dr. Felicia",
            "patients": {
                "id": 3,
                "name": "Sheila",
                "age": 45,
                "provider_id": 2
            }
        }
    ],
    "success": True,
    "total_providers": 1
}

#### POST '/patients'
Enter via Postman:
{
	"name": "Adele",
	"age": 55,
    "provider_id": 2
}
Returns via Postman:
{
    "success": True
}

#### PATCH '/patients/{id}'
Returns a success value. If the patient is not found,returns 404 Error.
Enter via Postman:
{
	"name": "Karina",
	"age": 65, 
    "provider_id": 1
}
Returns via Postman:
{
    "success": True
}

#### DELETE '/patients/{id}'
Return the patient id that was deleted and success value.
Returns via Postman:
{
        "success": True,
        "deleted": 2,
}

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The Auth0 Client ID
The JWT token contains the permissions for the 'Insurance Manager' and 'Insurance Agent' roles.