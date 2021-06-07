import os
from sqlalchemy import Column, String, Integer, \
  ForeignKey, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

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


'''
Provider: 
    name, insurance type, state, and phone
'''
class Provider(db.Model):  
  __tablename__ = 'providers'

  id = Column(Integer, primary_key=True)
  name = Column(String(120), nullable=False)
  state = Column(String(120), nullable=False)
  patients = relationship('patient', backref="provider", lazy=True)

  def __init__(self, name, state):
    self.name = name
    self.state = state
    self.patients = patients

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
      'state': self.state,
      'patients': list(map(lambda patient: patient.format(), self.patients))
    }

'''
Patient: 
    name, age, insurance type, and state
'''
class Patient(db.Model):  
  __tablename__ = 'patients'

  id = Column(Integer, primary_key=True)
  name = Column(String(120), nullable=False)
  age = Column(Integer, nullable=False)
  state = Column(String(120), nullable=False)
  provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)

  def __init__(self, name, age, state, provider_id):
    self.name = name
    self.age = age
    self.state = state
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
      'state': self.state,
      'provider_id': self.provider_id
    }