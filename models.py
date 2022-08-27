from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import aggregated

import json
from collections import namedtuple

db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(40)))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    shows = db.relationship('Show', backref='venues', cascade='all, delete-orphan' , lazy=True)

    @aggregated('num_upcoming_shows', db.Column(db.Integer))
    def num_upcoming_shows(self):
        return db.func.count('1')

    num_upcoming_shows = db.relationship('Show', backref='Venue')

    def __repr__(self):
        return f'< Venue  ID: {self.id} Name: {self.name} UPCOMING_shows: {self.num_upcoming_shows}>'

    def seed_data(self):
        Venue.query.delete()

        data1 = {
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],

            "address": "1015 Folsom Street",
            "city_id": 2,
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }
        data2 = {
            "name": "The Dueling Pianos Bar",
            "genres": ["Classical", "R&B", "Hip-Hop"],
            "address": "335 Delancey Street",
            "city_id": 1,
            "phone": "914-003-1132",
            "website": "https://www.theduelingpianos.com",
            "facebook_link": "https://www.facebook.com/theduelingpianos",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
        }
        data3 = {
            "name": "Park Square Live Music & Coffee",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city_id": 2,
            "phone": "415-000-1234",
            "website": "https://www.parksquarelivemusicandcoffee.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
        }

        venues = [data1,data2,data3]

        for data in venues:
            venue = Venue(**data)
            db.session.add(venue)

        db.session.commit()


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(40)))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    shows = db.relationship('Show', backref='artists', cascade='all, delete-orphan' , lazy=True)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))


    def seed_data(self):
        Artist.query.delete()

        data1 = {
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city_id": 2,
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        }
        data2 = {
            "name": "Matt Quevedo",
            "genres": ["Jazz"],
            "city_id": 1,
            "phone": "300-400-5000",
            "facebook_link": "https://www.facebook.com/mattquevedo923251523",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"

        }
        data3 = {
            "name": "The Wild Sax Band",
            "genres": ["Jazz", "Classical"],
            "city_id": 2,
            "phone": "432-325-5432",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
        }

        artists = [data1,data2,data3]

        for data in artists:
            artist = Artist(**data)
            db.session.add(artist)

        db.session.commit()


class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    venues = db.relationship('Venue', backref='city',  lazy=True)
    artist = db.relationship('Artist', backref='city', lazy=True)

    def __repr__(self):
        return self.city

    def seed_data(self):
        City.query.delete()
        cities = [{
            "city" : "New York",
            "state" : "NY"
        },
            {
                "city": "San Francisco",
                "state": "CA"
            }]

        for json_city in cities:
            city = City(**json_city)
            db.session.add(city)

        db.session.commit()


class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key= True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key= True)
    start_time = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Show ID: {self.venue_id} Artist_ID: {self.artist_id} Venue_ID: {self.venue_id} Start_time: {self.start_time} >'

    def seed_data(self):
        Show.query.delete()

        data = [{
            "venue_id": 1,
            "artist_id": 1,
            "start_time": "2019-05-21T21:30:00.000Z"
        }, {
            "venue_id": 3,
            "artist_id": 2,
            "start_time": "2019-06-15T23:00:00.000Z"
        }, {
            "venue_id": 3,
            "artist_id": 3,
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "artist_id": 1,
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 2,
            "artist_id": 3,
            "start_time": "2035-04-15T20:00:00.000Z"
        }]

        for show in data:
            show = Show(**show)
            db.session.add(show)

        db.session.commit()