from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///b20.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    a1 = db.Column(db.Integer)
    a2 = db.Column(db.Integer)
    a3 = db.Column(db.Integer)
    midterm = db.Column(db.Integer)
    remark = db.relationship('Remark', backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.username}', '{self.first_name}', '{self.last_name}')"


class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"Instructor('{self.username}', '{self.first_name}', '{self.last_name}')"


class Remark(db.Model):
    __tablename__ = 'Remark'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'Student.id'), nullable=False)
    student_first_name = db.Column(db.String(40), nullable=False)
    student_last_name = db.Column(db.String(40), nullable=False)
    item = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.Integer)
    reason = db.Column(db.String(1000), nullable=False)


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(1000), nullable=False)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/login-student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'GET':
        return render_template('login.html', type='student')


@app.route('/login-instructor', methods=['GET', 'POST'])
def login_instructor():
    if request.method == 'GET':
        return render_template('login.html', type='instructor')


@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'GET':
        return render_template('register.html', type='student')
    else:
        try:
            user = format_user(request.form)
            add_student(user)
            flash(
                f"Successfully registered {request.form['username']}.", 'success')
        except Exception as err:
            flash("This username already exists. Please choose a new one.", 'error')

        return render_template('register.html', type='student')


@app.route('/register-instructor', methods=['GET', 'POST'])
def register_instructor():
    if request.method == 'GET':
        return render_template('register.html', type='instructor')
    else:
        try:
            user = format_user(request.form)
            add_instructor(user)
            flash(
                f"Successfully registered {request.form['username']}.", 'success')
        except Exception as err:
            flash("This username already exists. Please choose a new one.", 'error')

        return render_template('register.html', type='instructor')


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


def add_student(user):
    user = Student(username=user[0], password=user[3],
                   first_name=user[1], last_name=user[2])
    db.session.add(user)
    db.session.commit()


def add_instructor(user):
    user = Instructor(username=user[0], password=user[3],
                      first_name=user[1], last_name=user[2])
    db.session.add(user)
    db.session.commit()


def format_user(request):
    password_hash = bcrypt.generate_password_hash(
        request['password'])
    user = (
        request['username'],
        request['first_name'],
        request['last_name'],
        password_hash
    )
    return user


if __name__ == '__main__':
    app.run(debug=True)
