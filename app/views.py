from flask import Flask, render_template, redirect, url_for, request, session
from app import app, recommender, ratings, mood_calc, models
import os, uuid

valid_genres = ['Rock','Folk', 'Blues', 'Pop', 'Country', 'Hip-hop', 'Jazz', 'SoulRB', 'Classical', 'Instrumental', 'Electronic', 'Experimental', 'International', 'Spoken']

@app.route('/')
def index():
    redirect_index = redirect(url_for('genre'))
    return redirect_index

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    title = 'Music Player | Preferences'

    session['user_session_id'] = str(uuid.uuid4()) # user_session_id for Session model
    
    if request.method == 'POST':
        selected_genres = request.form.getlist('genre')
        session['selected_genres'] = selected_genres # liked_genres for Session model
        
        # Genre
        user_selected_weights = []

        # Get the selected genres from the user
        selected_genre_count = len(selected_genres)

        # Weigh the genres equally based on the users selection.
        for genre in valid_genres:
            if genre in selected_genres:
                user_selected_weights.append(1/selected_genre_count)  # Equal weight for each selected genre (fe. 0.5 for 2 genres)
            else:
                user_selected_weights.append(0) # No weight for non-selected genres (no chance)

        session['user_selected_weights'] = user_selected_weights
        session['ratings_impact_genre'] = user_selected_weights
        session['ratings_impact_genre_normalized'] = user_selected_weights
        return redirect(url_for('mood', genre=selected_genres,))

    return render_template('genre.html', title=title, genres=valid_genres)

@app.route('/mood', methods=['GET', 'POST'])
def mood():
    title = 'Music Player | Mood'
    moods = ['Nervous', 'Angry', 'Annoyed', 'Excited', 'Happy', 'Pleased', 'Relaxed', 'Peaceful', 'Calm', 'Sad', 'Bored', 'Sleepy']

    if request.method == 'POST':
        selected_moods = request.form.getlist('mood')
        session['selected_moods'] = selected_moods

        # Calculate the users mood
        users_mood = mood_calc.mood_calc()
        session['users_mood'] = users_mood
        session['ratings_impact_mood'] = users_mood # initially calculated user mood

        return redirect(url_for('player', genre=session['selected_genres'], mood=selected_moods))
    
    return render_template('mood.html', moods=moods, title=title)

@app.route('/player')
def player():
    title = 'Music Player | Playing...'
    excerpts_dir = "app/static/assets/excerpts"

    audio_files = [file for file in os.listdir(excerpts_dir) if file.endswith('.mp3')]

    #  Recommender system
    recommended_song, song_info = recommender.recommend_song(audio_files, valid_genres)

    session['curr_song_info'] = song_info

    return render_template('player.html', title=title, recommended_song=recommended_song)

@app.route('/submit_ratings', methods=['POST'])
def submit_ratings():
    rating = request.form['rating']

    session['rating'] = rating
    ratings.user_ratings(valid_genres)



    # Store in the database
    user_session_id = session['user_session_id']
    song_id = session['curr_song_info']['song_id']
    mood_shift_after_rating = session['users_mood_after_each_rating']
    user_rating = session['rating']
    liked_genres = session['selected_genres']
    mood_chosen = session['users_mood']
    final_mood_shift = session['final_users_mood']
    # discovered_genres = session['']

    models.Session.create_session(user_session_id, liked_genres, mood_chosen, final_mood_shift, discovered_genres)
    models.Ratings.create_rating(song_id, mood_shift_after_rating, discovered_genres, user_rating, user_session_id)
    
    return redirect(url_for('player'))
