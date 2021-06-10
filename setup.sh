export AUTH0_DOMAIN="lgaetano.us.auth0.com"
export ALGORITHMS=["RS256"]
export API_AUDIENCE="capstone"

# export DATABASE_URL="postgres://postgres@localhost:5432/capstone"
export DATABASE_URL="postgresql://postgres@localhost:5432/capstone"

export FLASK_APP=app.py
export FLASK_ENVIRONMENT=debug