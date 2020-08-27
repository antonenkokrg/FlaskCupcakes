"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime,Float

db = SQLAlchemy()

DEFAULT_IMAGE = "https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg"


class Cupcake(db.Model):
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text,nullable=False, default=DEFAULT_IMAGE)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)