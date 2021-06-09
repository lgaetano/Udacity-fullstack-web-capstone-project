export AUTH0_DOMAIN="lgaetano.us.auth0.com"
export ALGORITHMS=["RS256"]
export API_AUDIENCE="capstone"

export DATABASE_URL="postgres://postgres@localhost:5432/capstone"
# export DATABASE_URL="postgresql://postgres@localhost:5432/capstone"
# export DATABASE_URL="postgres:///JKLMNOPQ:some_value@ec2-XX-YYY-ZZ-AA.compute-1.amazonaws.com:5432/ABCDEFGHI"

export FLASK_APP=app.py
export FLASK_ENVIRONMENT=debug