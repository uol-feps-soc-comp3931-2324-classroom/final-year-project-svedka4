from app import db
import datetime

class Session(db.Model):
    user_session_id = db.Column(db.String, primary_key=True)
    liked_genres = db.Column(db.String)
    mood_chosen = db.Column(db.String)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)


class Ratings(db.Model):
    current_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    song_id = db.Column(db.String, primary_key=True)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)
    user_rating = db.Column(db.String)
    user_session_id = db.Column(db.String, db.ForeignKey('session'), primary_key=True)
    session = db.relationship('Session', backref='ratings')
