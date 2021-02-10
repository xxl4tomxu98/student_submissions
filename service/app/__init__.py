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
def get_completed_assignments_count(student_id):
    student = Student.query.get_or_404(student_id)
    all_courses = student.enrolled_courses
    print(all_courses)
    all_assignments_matrix = [course.course_works for course in all_courses]
    print(all_assignments_matrix)
    all_assignments_flatten = [assign for sublist in all_assignments_matrix
                               for assign in sublist]
    print(all_assignments_flatten)
    all_submissions_matrix = [assign.work_submissions for assign
                              in all_assignments_flatten]
    all_submissions_flatten = [sub for sublist in all_submissions_matrix
                               for sub in sublist]
    print(all_submissions_flatten)
    student_completed_assignments = [submission
                    for submission in all_submissions_flatten
                    if submission.type == 'TURNED_IN']
    student_completed_assignments_count = len(student_completed_assignments)
    return {'count': student_completed_assignments_count,
            'completed_assignments': [assign.to_dict() for assign in
                                       student_completed_assignments]}


@app.route('/courses/<int:course_id>')
def avg_grade(course_id):
    course = Course.query.filter_by(id = course_id).first()
    all_students = course.signedup_students
    all_submissions_matrix = [[submission for submission in
                               student.student_submissions]
                              for student in all_students]
    all_submissions_flatten = [sub for sublist in all_submissions_matrix
                               for sub in sublist]
    all_grades = [s.assigned_points for s in all_submissions_flatten]
    if len(all_grades) != 0:
        return "{:3.1f}".format(sum(all_grades)/len(all_grades))
    return 0
