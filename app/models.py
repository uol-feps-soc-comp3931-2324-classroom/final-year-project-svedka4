from app import db
import datetime, json

class Session(db.Model):
    __tablename__ = 'session'

    user_session_id = db.Column(db.String, primary_key=True)
    liked_genres = db.Column(db.String)
    mood_chosen = db.Column(db.String)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)

    @staticmethod
    def session_exists(user_session_id):
        return Session.query.filter_by(user_session_id=user_session_id).first() is not None

    @staticmethod
    def create_session(user_session_id, liked_genres, mood_chosen, mood_shift, discovered_genres):
        session_instance = Session(
            user_session_id=user_session_id,
            liked_genres=json.dumps(liked_genres),  # Convert list to JSON string
            mood_chosen=json.dumps(mood_chosen),    # Convert tuple to JSON string
            mood_shift=json.dumps(mood_shift),      # Convert tuple to JSON string
            discovered_genres=json.dumps(discovered_genres)
        )
        db.session.add(session_instance)
        db.session.commit()

class Ratings(db.Model):
    __tablename__ = 'ratings'

    current_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    song_id = db.Column(db.String, primary_key=True)
    mood_shift = db.Column(db.String)
    discovered_genres = db.Column(db.String)
    serendipity_rating = db.Column(db.String)
    user_rating = db.Column(db.String)
    user_session_id = db.Column(db.String, db.ForeignKey('session'), primary_key=True)
    session = db.relationship('Session', backref='ratings')

    @staticmethod
    def create_rating(song_id, mood_shift, discovered_genres, serendipity_rating, user_rating, user_session_id):
        rating_instance = Ratings(
            song_id=song_id,
            mood_shift=json.dumps(mood_shift),  # Convert tuple to JSON string
            discovered_genres=json.dumps(discovered_genres),  # Convert list to JSON string
            serendipity_rating=serendipity_rating,
            user_rating=user_rating,
            user_session_id=user_session_id
        )
        db.session.add(rating_instance)
        db.session.commit()