from app import db

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    genres = db.relationship('Genre', backref='participant', lazy='dynamic')
    moods = db.relationship('Mood', backref='participant', lazy='dynamic')
    ratings = db.relationship('Ratings', backref='participant', lazy='dynamic')

    def __repr__(self):
        return '<Participant %r>' % (self.name)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    genre = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Genre %r>' % (self.name)
    
class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    mood = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Mood %r>' % (self.name)

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    song_id = db.Column(db.Integer)
    rating = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Rating %r>' % (self.name)