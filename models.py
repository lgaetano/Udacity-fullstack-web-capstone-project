from sqlalchemy import Column, String, create_engine
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
Provider: name, insurance type, state, and phone
'''
class Provider(db.Model):  
  __tablename__ = 'Provider'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  insurance = Column(String, nullable=False)
  state = Column(String, nullable=False)
  phone = Column(String, nullable=False)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'insurance': self.insurance,
      'state': self.state,
      'phone': self.state
      }