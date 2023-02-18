from .extensions import db
from datetime import datetime

class Blurb(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  content = db.Column(db.String(150), nullable=False)
  datetime = db.Column(db.DateTime(), default=datetime.now)