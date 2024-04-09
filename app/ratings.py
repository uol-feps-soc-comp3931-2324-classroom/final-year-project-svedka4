from flask import session

# love, like, neutral, dislike, hate
ratings = {
    'love': 1,
    'like': 0.5,
    'neutral': 0,
    'dislike': -0.5,
    'hate': -1
}

def user_ratings():
    current_song = session['curr_song_info']
    user_ratings = session['rating']
    print(current_song, user_ratings)

    print(session['ratings_impact_genre'])

    # Keep track of the impact of ratings on users mood
    impact_mood = session['ratings_impact_mood']

    mood_shift = 0.05 * ratings[user_ratings]

    # Nudge the users mood towards the mood of the song if they like it
    difference = [current_song['valence'] - impact_mood[0], current_song['arousal'] - impact_mood[1]]
    normalized_difference = [difference[0] / (difference[0]**2 + difference[1]**2)**0.5, difference[1] / (difference[0]**2 + difference[1]**2)**0.5]
    push = (normalized_difference[0] * mood_shift, normalized_difference[1] * mood_shift)

    new_impact_mood = (impact_mood[0] + push[0], impact_mood[1] + push[1])
    session['ratings_impact_mood'] = new_impact_mood

    print("Song Valence: ", current_song['valence'], "Song Arousal: ", current_song['arousal'])
    print("Users Valence", impact_mood[0], "Users Arousal", impact_mood[1])
    print("New Valence", new_impact_mood[0], "New Arousal", new_impact_mood[1])

    # if a user loves - give same weight to the genre as initially chosen genres
    # if a user likes - give 0.5 weight to the genre
    # if a user is neutral or dislikes or hates a recommendation - give 0 weight to the genre





