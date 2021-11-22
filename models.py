from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __str__(self) -> str:
        return f"User {self.id}: {self.name}"

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    plant_type = db.Column(db.String(1000))
    last_watered = db.Column(db.DateTime)
    moisture_level = db.Column(db.String(100))
    #audio_count = db.Column(db.Integer, default=0)

    def __str__(self):
        return f"Plant {self.id}: {self.plant_type}"