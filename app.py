from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', page='home')

@app.route('/team')
def team():
    return render_template('team.html', page='team')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', page='calendar')

@app.route('/announcements')
def announcements():
    return render_template('announcements.html', page='announcements')

@app.route('/grades')
def grades():
    return 'grades'

@app.route('/lectures')
def lectures():
    return render_template('lectures.html', page='lectures')

@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html', page='tutorials')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html', page='assignments')

@app.route('/tests')
def tests():
    return render_template('tests.html', page='tests')

@app.route('/faq')
def faq():
    return render_template('faq.html', page='faq')

@app.route('/resources')
def resources():
    return render_template('resources.html', page='resources')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', page='feedback')

if __name__ == '__main__':
    app.run(debug=True)