from flask import Flask, jsonify
from .models import db, Submission, Student, Course, Course_work, rosters
from os import environ
from sqlalchemy import or_, String
from sqlalchemy.sql.expression import cast

# use config class to connect sqlAlchemy to postgresql database
class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or \
        "postgresql://records_app:password@localhost/records"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


# test route
@app.route('/')
def hello():
    return "Hello World!"


# This is a multi-purpose search engine that can return
# movies based on match on title, genres, or movie_id(return one)


@app.route('/students')
def get_students():
    response = Student.query.all()
    return {'list': [s.to_dict() for s in response]}


@app.route('/courses')
def get_courses():
    response = Course.query.all()
    return {'list': [c.to_dict() for c in response]}


@app.route('/submissions')
def get_submissions():
    response = Submission.query.all()
    return {'list': [sub.to_dict() for sub in response]}


@app.route('/assignments')
def get_assignments():
    response = Course_work.query.all()
    return {'list': [a.to_dict() for a in response]}


@app.route('/submissions/<id>')
def get_submission_from_id(id):
    submission = Submission.query.filter_by(id=id).first()
    return {'submission': submission.to_dict()}


@app.route('/students/<int:student_id>')
def get_completed_assignments(student_id):

    student = Student.query.filter_by(id = student_id).first()

    return {'result': cast(student.completed_assigment_count, String)}
