from app import db
import datetime
from flask import session

class Session(db.Model):
    __tablename__ = 'session'

    user_session_id = db.Column(db.String, primary_key=True)
    liked_genres = db.Column(db.String)
    mood_chosen = db.Column(db.String)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)

    @staticmethod
    def create_session(user_session_id, liked_genres, mood_chosen, mood_shift, discovered_genres):
        session_instance = Session(
            user_session_id=user_session_id,
            liked_genres=liked_genres,
            mood_chosen=mood_chosen,
            mood_shift=mood_shift,
            discovered_genres=discovered_genres
        )
        db.session.add(session_instance)
        db.session.commit()

class Ratings(db.Model):
    __tablename__ = 'ratings'

    current_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    song_id = db.Column(db.String, primary_key=True)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)
    user_rating = db.Column(db.String)
    user_session_id = db.Column(db.String, db.ForeignKey('session'), primary_key=True)
    session = db.relationship('Session', backref='ratings')

    @staticmethod
    def create_rating(song_id, mood_shift, discovered_genres, user_rating, user_session_id):
        rating_instance = Ratings(
            song_id=song_id,
            mood_shift=mood_shift,
            discovered_genres=discovered_genres,
            user_rating=user_rating,
            user_session_id=user_session_id
        )
        db.session.add(rating_instance)
        db.session.commit()