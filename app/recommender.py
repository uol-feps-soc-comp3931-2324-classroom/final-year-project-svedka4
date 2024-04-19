from flask import session
import csv
import random
from app import mood_calc

csv_file = 'app/static/assets/dataset.csv'

song_info = {}

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
                'song_id': row[0],
                'main_genre': main_genre,
                'sub_genres': sub_genres,
                'arousal': float(row[2]),
                'valence': float(row[3])
            }


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

# The module for picking genre. (Not finshed yet, could do with adding the serendipity for discovered genres)
def recommend_song(audio_files, valid_genres):
    
    # Read the CSV
    if song_info == {}:
        read_csv()

    user_selected_weights = session['ratings_impact_genre_normalized']

    found_song = False
    accurate_recommendation = None

    while not found_song:
        print("Finding song")
        # Pick a random genre based on the users selection
        picked_genre = random.choices(valid_genres, weights=user_selected_weights)[0] # Pick a random genre based on the weights

        # Filter the audio files based on the picked genre
        # if song played - don't play it again

        filtered_genre_audio_files = [] 
        
        for file in audio_files:         
            if picked_genre == song_info[file[:-4]]['main_genre'] and file not in session['played_songs']:
                filtered_genre_audio_files.append(file)

        users_mood = session['ratings_impact_mood']

        filtered_mood_audio_files = []
        
        for audio_file in filtered_genre_audio_files:
            song = song_info[audio_file[:-4]]
            cosine_similarity = (users_mood[0] * song['valence'] + users_mood[1] * song['arousal']) / ((users_mood[0]**2 + users_mood[1]**2)**0.5 * (song['valence']**2 + song['arousal']**2)**0.5)
            # filter the audio files based on the cosine similarity
            if cosine_similarity > 0.6:
            # if distance < 0.2: 
                filtered_mood_audio_files.append(audio_file)

            if len(filtered_mood_audio_files) > 0:
                found_song = True
                accurate_recommendation = random.choice(filtered_mood_audio_files)
                break

    print('Session played songs:', session['played_songs'])
    session['played_songs'][accurate_recommendation] = True

    return accurate_recommendation, song_info[accurate_recommendation[:-4]]


