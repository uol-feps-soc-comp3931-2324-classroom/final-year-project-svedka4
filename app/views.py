from flask import Flask, render_template, redirect, url_for, request, session
from app import app, recommender
import os

valid_genres = ['Rock', 'Pop', 'Country', 'Hip-hop', 'Jazz', 'Classical', 'Electronic', 'Folk', 'Blues']

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    title = 'Music Player | Preferences'

    if request.method == 'POST':
        selected_genres = request.form.getlist('genre')
        session['selected_genres'] = selected_genres
        return redirect(url_for('mood', genre=selected_genres,))

    return render_template('genre.html', title=title, genres=valid_genres)

@app.route('/mood', methods=['GET', 'POST'])
def mood():
    title = 'Music Player | Mood'
    moods = ['Nervous', 'Angry', 'Annoyed', 'Excited', 'Happy', 'Pleased', 'Relaxed', 'Peaceful', 'Calm', 'Sad', 'Bored', 'Sleepy']

    if request.method == 'POST':
        selected_moods = request.form.getlist('mood')

        session['selected_moods'] = selected_moods
  
        return redirect(url_for('player', genre=session['selected_genres'], mood=selected_moods))
    
    return render_template('mood.html', moods=moods, title=title)

@app.route('/player')
def player():
    title = 'Music Player | Playing...'
    excerpts_dir = "app/static/assets/excerpts"

    audio_files = [file for file in os.listdir(excerpts_dir) if file.endswith('.mp3')]




    #  Recommender system
    recommender.pick_song_genre(audio_files, valid_genres)

    return render_template('player.html', title=title, audio_files=audio_files)