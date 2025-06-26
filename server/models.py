# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user', lazy=True)

    @hybrid_property
    def password(self):
        raise AttributeError('Password cannot be accessed.')

    @password.setter
    def password(self, password_plaintext):
        self._password_hash = bcrypt.generate_password_hash(password_plaintext).decode('utf-8')

    def authenticate(self, password_plaintext):
        return bcrypt.check_password_hash(self._password_hash, password_plaintext)

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    __table_args__ = (
        CheckConstraint('length(instructions) >= 50', name='check_instructions_length'),
    )
