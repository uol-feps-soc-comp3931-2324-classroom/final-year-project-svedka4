from flask import session
import csv
import random

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
def pick_song_genre(audio_files, valid_genres):
    
    # Read the CSV
    if song_info == {}:
        read_csv()

    user_selected_weights = []

    # Get the selected genres from the user
    selected_genres = session['selected_genres']
    selected_genre_count = len(selected_genres)

    # Weigh the genres equally based on the users selection.
    for genre in valid_genres:
        if genre in selected_genres:
            user_selected_weights.append(1/selected_genre_count)
        else:
            user_selected_weights.append(0)

    # Pick a random genre based on the users selection
    picked_genre = random.choices(valid_genres, weights=user_selected_weights, k=1)[0]
 
    # Filter the audio files based on the picked genre
    filtered_audio_files = [file for file in audio_files if picked_genre == song_info[file[:-4]]['main_genre']]


    random_song = random.choice(filtered_audio_files)
    print('Random song:', random_song)
    print(song_info[random_song[:-4]])

    return filtered_audio_files


