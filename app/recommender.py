from flask import session
import csv
import random
from app import mood_calc, serendipity

csv_file = 'app/static/assets/dataset.csv'

song_info = {}


user_selected_genres = []
user_selected_weights = []

discovered_genres = []

def read_csv():
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            
            if row[0] == 'song_id':
                continue

            genres = row[1].split('-')

            main_genre = genres[0]
            sub_genres = genres[1:]

            song_info[row[0]] = {
                'main_genre': main_genre,
                'sub_genres': sub_genres,
                'arousal': float(row[2]),
                'valence': float(row[3])
            }


# The module for picking genre. (Not finshed yet, could do with adding the serendipity for discovered genres)
def recommend_song(audio_files, valid_genres):
    
    # Read the CSV
    if song_info == {}:
        read_csv()

    #Genre
    user_selected_weights = []

    # Get the selected genres from the user
    selected_genres = session['selected_genres']
    selected_genre_count = len(selected_genres)

    # Weigh the genres equally based on the users selection.
    for genre in valid_genres:
        if genre in selected_genres:
            user_selected_weights.append(1/selected_genre_count)  # Equal weight for each selected genre (fe. 0.5 for 2 genres)
        else:
            user_selected_weights.append(0) # No weight for non-selected genres (no chance)

    # Pick a random genre based on the users selection
    picked_genre = random.choices(valid_genres, weights=user_selected_weights)[0] # Pick a random genre based on the weights

    # Filter the audio files based on the picked genre
    filtered_genre_audio_files = [file for file in audio_files if picked_genre == song_info[file[:-4]]['main_genre']]


    # Calculate the users mood
    users_mood = mood_calc.mood_calc()
    session['users_mood'] = users_mood

    filtered_mood_audio_files = []
    
    for audio_file in filtered_genre_audio_files:
        song = song_info[audio_file[:-4]]
        cosine_similarity = (users_mood[0] * song['valence'] + users_mood[1] * song['arousal']) / ((users_mood[0]**2 + users_mood[1]**2)**0.5 * (song['valence']**2 + song['arousal']**2)**0.5)
        # filter the audio files based on the cosine similarity
        if cosine_similarity > 0.6:
        # if distance < 0.2: 
            filtered_mood_audio_files.append(audio_file)

    accurate_recommendation = random.choice(filtered_mood_audio_files)

    serendipitous_recommendation = serendipity()

    return serendipitous_recommendation


