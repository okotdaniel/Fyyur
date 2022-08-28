from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import aggregated

import json
from collections import namedtuple

db = SQLAlchemy()



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(db.PickleType())
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent=db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.Text())

    def __repr__(self) -> str:
      return f'<Venue ID: {self.id}, Name: {self.name} >'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(db.PickleType())
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue=db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.Text())
    show = db.relationship('Shows')

    def __repr__(self) -> str:
      return f'<Artist ID: {self.id}, Name: {self.name} >'
 

class Shows(db.Model):
  __tablename__ = 'Shows'

  start_time = db.Column(db.DateTime(timezone=True))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  venue = db.relationship("Venue")

  def __repr__(self) -> str:
    return f'<Venue ID: {self.venue_id}, Artist ID: {self.artist_id}, StartTime: {self.start_time}>'
