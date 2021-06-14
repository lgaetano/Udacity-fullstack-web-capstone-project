from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    migrate = Migrate(app, db)

'''
Provider: 
    name, insurance type, state, and phone
'''
class Provider(db.Model):  
  __tablename__ = 'providers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  patients = db.relationship('Patient', backref="provider", lazy=True)

  def __init__(self, name, state):
    self.name = name

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'patients': list(map(lambda patient: patient.format(), self.patients))
    }

'''
Patient: 
    name, age, insurance type, and state
'''
class Patient(db.Model):  
  __tablename__ = 'patients'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)

  def __init__(self, name, age, provider_id):
    self.name = name
    self.age = age
    self.provider_id = provider_id

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'provider_id': self.provider_id
    }