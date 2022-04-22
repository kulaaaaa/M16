# blog/models.py

from . import db
import datetime
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(100), index=True, unique=True)
   email = db.Column(db.String(200), index=True, unique=True)
   password_hash = db.Column(db.String(128))

   def __str__(self):
       return f"<User {self.username}>"
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)