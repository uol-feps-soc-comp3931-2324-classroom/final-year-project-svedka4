from flask import session

emotion_mapping = {
    # valence - X, arousal - Y
    'excited': (0.357357, 0.744744),
    'happy': (0.555555, 0.540540),
    'pleased': (0.738738, 0.282282),

    'annoyed': (-0.390390, 0.744744),
    'angry': (-0.660660, 0.519519),
    'nervous': (-0.726726, 0.264264),

    'sad': (-0.702702, -0.384384),
    'bored': (-0.462462, -0.603603),
    'sleepy': (-0.228228, -0.801801),

    'relaxed': (0.705705, -0.0348348),
    'peaceful': (0.549549, -0.549549),
    'calm': (0.291291, -0.732732)
}

def users_average_emotion(emotions):
    valence = 0
    arousal = 0
    for emotion in emotions:
        valence += emotion_mapping[emotion.lower()][0]
        arousal += emotion_mapping[emotion.lower()][1]
    return (valence/len(emotions), arousal/len(emotions))

def mood_calc():
    selected_moods = session['selected_moods']
    recommendation_mood = users_average_emotion(selected_moods)
    return recommendation_mood