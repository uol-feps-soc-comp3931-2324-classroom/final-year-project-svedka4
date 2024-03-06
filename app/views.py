from flask import Flask, render_template, redirect, url_for, request
from app import app

@app.route('/')
def genre():
    genres = ['Rock', 'Pop', 'Country', 'Hip-hop', 'Jazz', 'Classical', 'Electronic', 'Folk', 'Blues']
    return render_template('genre.html', genres=genres)

@app.route('/mood', methods=['POST'])
def mood():
    moods = ['Nervous', 'Angry', 'Annoyed', 'Excited', 'Happy', 'Pleased', 'Relaxed', 'Peaceful', 'Calm', 'Sad', 'Bored', 'Sleepy']
    selected_genre = request.form.getlist('genre')
    return render_template('mood.html', selected_genre=selected_genre, moods=moods)