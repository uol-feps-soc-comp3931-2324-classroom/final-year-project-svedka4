from flask import session

# love, like, neutral, dislike, hate
ratings = {
    'love': 1,
    'like': 0.5,
    'neutral': 0,
    'dislike': -0.5,
    'hate': -1
}

def user_ratings(valid_genres):
    current_song = session['curr_song_info']
    user_ratings = session['rating']

    # Keep track of the impact of ratings on users mood
    impact_mood = session['ratings_impact_mood'] # initially calculated user mood

    mood_shift = 0.05 * ratings[user_ratings]

    # Nudge/push the users mood towards the mood of the song if they like it
    difference = [current_song['valence'] - impact_mood[0], current_song['arousal'] - impact_mood[1]]
    normalized_difference = [difference[0] / (difference[0]**2 + difference[1]**2)**0.5, difference[1] / (difference[0]**2 + difference[1]**2)**0.5]
    push = (normalized_difference[0] * mood_shift, normalized_difference[1] * mood_shift)

    users_mood_after_each_rating = (impact_mood[0] + push[0], impact_mood[1] + push[1])
    # where the user is at after a nudge
    session['users_mood_after_each_rating'] = users_mood_after_each_rating
    session['final_user_mood'] = users_mood_after_each_rating

    # Keep track of the impact of ratings on users genre preferences; store only discovered genres
    impact_genre = session['ratings_impact_genre'] # initial weights on picked genres


    # if a user likes a song - give the main genre weight 
    for i in range(len(valid_genres)):
        if valid_genres[i] == current_song['main_genre']:
            impact_genre[i] += ratings[user_ratings] * 0.25
            impact_genre[i] = max(0, impact_genre[i])

    # if a liked song has subgenres - give them weight
    if len(current_song['sub_genres']) > 0:
        for i in range(len(valid_genres)):
            if valid_genres[i] in current_song['sub_genres']:
                impact_genre[i] += ratings[user_ratings] * 0.25
                impact_genre[i] = max(0, impact_genre[i])

    session['ratings_impact_genre'] = impact_genre 

    normalized_ratings_impact_genre = []
    total = sum(impact_genre)

    for i in range(len(impact_genre)):
        normalized_ratings_impact_genre.append(impact_genre[i] / total)
        
    print("Normalized:", normalized_ratings_impact_genre)
    session['ratings_impact_genre_normalized'] = normalized_ratings_impact_genre

    # Discovered genres mapping to weights after rating impact
    selected_genres = session['selected_genres']

    gained_weight_indices = [i for i, weight in enumerate(normalized_ratings_impact_genre) if weight > 0]
    gained_weight_genres = [valid_genres[i] for i in gained_weight_indices]

    discovered_genres = [genre for genre in gained_weight_genres if genre not in selected_genres]
    session['discovered_genres'] = discovered_genres

