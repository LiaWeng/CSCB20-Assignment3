from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '66556A586E3272357538782F413F4428'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
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
    student_username = db.Column(db.String(20), db.ForeignKey(
        'Student.username'), nullable=False)
    student_first_name = db.Column(db.String(40), nullable=False)
    student_last_name = db.Column(db.String(40), nullable=False)
    item = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.Integer)
    reason = db.Column(db.String(1000), nullable=False)


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    instructor_username = db.Column(db.String(20), db.ForeignKey(
        'Instructor.username'), nullable=False)
    q1 = db.Column(db.String(1000), nullable=False)
    q2 = db.Column(db.String(1000), nullable=False)
    q3 = db.Column(db.String(1000), nullable=False)
    q4 = db.Column(db.String(1000), nullable=False)


@app.route('/')
def root():
    if 'user' in session:
        return render_template('home.html')
    else:
        return render_template('root.html')


@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'GET':
        return render_template('register.html', type='student')
    else:
        return register(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['password'], 'student')


@app.route('/register-instructor', methods=['GET', 'POST'])
def register_instructor():
    if request.method == 'GET':
        return render_template('register.html', type='instructor')
    else:
        return register(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['password'], 'instructor')


@app.route('/login-student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'GET':
        return render_template('login.html', type='student')
    else:
        return login(request.form['username'], request.form['password'], 'student')


@app.route('/login-instructor', methods=['GET', 'POST'])
def login_instructor():
    if request.method == 'GET':
        return render_template('login.html', type='instructor')
    else:
        return login(request.form['username'], request.form['password'], 'instructor')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('type', None)
    return render_template('root.html')


@app.route('/home')
def home():
    check_authorization()
    return render_template('home.html', page='home')


@app.route('/grades', methods=['GET', 'POST'])
def grades():
    check_authorization()
    remarks = get_remarks()
    students = get_allstudents()

    if request.method == 'GET':
        if session['type'] == 'student':
            student = get_student(session['user'])
            return render_template('grades_s.html', page='grades', student=student)
        else:
            return render_template('grades_i.html', page='grades', remarks=remarks, students=students)
    else:
        return add_grades(request.form["student"], request.form["a1"], request.form["a2"], request.form["a3"], request.form["midterm"], students=students)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    check_authorization()
    instructors = get_instructors()

    if request.method == 'GET':
        if session['type'] == 'student':
            return render_template('feedback_s.html', page='feedback', instructors=instructors)
        else:
            feedbacks = get_feedback(session['user'])
            return render_template('feedback_i.html', page='feedback', feedbacks=feedbacks)
    else:
        return add_feedback(request.form["instructor"], request.form["q1"], request.form["q2"], request.form["q3"], request.form["q4"], instructors)


@app.route('/team')
def team():
    check_authorization()
    return render_template('team.html', page='team')


@app.route('/calendar')
def calendar():
    check_authorization()
    return render_template('calendar.html', page='calendar')


@app.route('/announcements')
def announcements():
    check_authorization()
    return render_template('announcements.html', page='announcements')


@app.route('/lectures')
def lectures():
    check_authorization()
    return render_template('lectures.html', page='lectures')


@app.route('/tutorials')
def tutorials():
    check_authorization()
    return render_template('tutorials.html', page='tutorials')


@app.route('/assignments')
def assignments():
    check_authorization()
    return render_template('assignments.html', page='assignments')


@app.route('/tests')
def tests():
    check_authorization()
    return render_template('tests.html', page='tests')


@app.route('/faq')
def faq():
    check_authorization()
    return render_template('faq.html', page='faq')


@app.route('/resources')
def resources():
    check_authorization()
    return render_template('resources.html', page='resources')


def register(username, first_name, last_name, password, type_user):
    password_hash = bcrypt.generate_password_hash(password)

    try:
        if type_user == 'student':
            user = Student(username=username,
                           first_name=first_name, last_name=last_name, password=password_hash)
        else:
            user = Instructor(username=username,
                              first_name=first_name, last_name=last_name, password=password_hash)

        db.session.add(user)
        db.session.commit()

        flash(
            f"Successfully registered {request.form['username']}.", 'success')
    except Exception as err:
        flash("This username already exists. Please choose a new one.", 'error')

    return render_template('register.html', type=type_user)


def login(username, password, type_user):
    session.pop('user', None)
    session.pop('type', None)

    if type_user == 'student':
        user = Student.query.filter_by(
            username=username).first()
    else:
        user = Instructor.query.filter_by(
            username=username).first()

    if not user:
        flash("Username does not exist.", 'error')
        return render_template('login.html', type=type_user)
    elif not bcrypt.check_password_hash(
            user.password, password):
        flash("Incorrect password.", 'error')
        return render_template('login.html', type=type_user)
    else:
        session['user'] = user.username
        session['type'] = type_user
        session.permanent = True
        return redirect(url_for('home'))


def check_authorization():
    if "user" not in session:
        abort(403, "Please sign in to access this page.")


def add_feedback(instructor, q1, q2, q3, q4, instructors):
    try:
        feedback = Feedback(instructor_username=instructor,
                            q1=q1, q2=q2, q3=q3, q4=q4)
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for submitting your feedback.", 'success')
    except Exception as err:
        flash("Error submitting feedback.", 'error')

    return render_template('feedback_s.html', page='feedback', instructors=instructors)


def get_instructors():
    return Instructor.query.all()


def get_student(username):
    return Student.query.filter_by(username=username).first()


def get_allstudents():
    return Student.query.all()


def get_remarks():
    return Remark.query.all()


def add_grades(username, a1, a2, a3, midterm, students):
    remarks = get_remarks()
    try:
        student = Student.query.filter_by(username=username).first()
        student.a1 = a1
        student.a2 = a2
        student.a3 = a3
        student.midterm = midterm
        db.session.commit()
        flash("Grades submitted successfully.", 'success')
    except Exception as err:
        flash("Error submitting grades.", 'error')
    return render_template('grades_i.html', page='grades', grades=grades, students=students, remarks=remarks)



def get_feedback(username):
    return Feedback.query.filter_by(instructor_username=username)


if __name__ == '__main__':
    app.run(debug=True)
