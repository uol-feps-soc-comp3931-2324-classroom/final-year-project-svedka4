from flask import Flask, render_template, redirect, url_for, request
from app import app
import os

@app.route('/')
def genre():
    title = 'Music Player | Preferences'
    genres = ['Rock', 'Pop', 'Country', 'Hip-hop', 'Jazz', 'Classical', 'Electronic', 'Folk', 'Blues']
    return render_template('genre.html', genres=genres, title=title)

@app.route('/mood')
def mood():
    title = 'Music Player | Mood'
    moods = ['Nervous', 'Angry', 'Annoyed', 'Excited', 'Happy', 'Pleased', 'Relaxed', 'Peaceful', 'Calm', 'Sad', 'Bored', 'Sleepy']
    # selected_genre = request.form.getlist('genre')
    return render_template('mood.html', moods=moods, title=title)

@app.route('/player')
def player():
    title = 'Music Player | Playing...'
    excerpts_dir = "app/static/assets/excerpts"
    audio_files = [file for file in os.listdir(excerpts_dir) if file.endswith('.mp3')]
    return render_template('player.html', title=title, audio_files=audio_files)