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
    student_completed_assignments_count = student.completed_assignments
    return {'count': student_completed_assignments_count}


@app.route('/courses/<int:course_id>')
def avg_grade(course_id):
    course = Course.query.get_or_404(course_id)
    all_students = course.signedup_students
    print(all_students)
    all_submissions_matrix = [student.student_submissions
                              for student in all_students]
    all_submissions_flatten = [sub for sublist in all_submissions_matrix
                               for sub in sublist]
    valid_submissions = [sub for sub in all_submissions_flatten
                         if sub.course_id == course_id]
    print(all_submissions_flatten)
    print(valid_submissions)
    all_grades = [s.assigned_points for s in valid_submissions]
    print(all_grades)
    if len(all_grades) != 0:
        return "{:3.1f}".format(sum(all_grades)/len(all_grades))
    return 0


@app.route('/teachers/<int:teacher_id>')
def all_created_assigments_count(teacher_id):
    all_courses = Course.query.filter(Course.teacher_id == teacher_id).all()
    print(all_courses)
    all_assignments_matrix = [course.course_works for course in all_courses]
    print(all_assignments_matrix)
    all_assignments_flatten = [assign for sublist in all_assignments_matrix
                               for assign in sublist]
    print(all_assignments_flatten)
    all_created_assignments_count = len(all_assignments_flatten)
    return {'teacher_created_assignments_count': all_created_assignments_count,
            'created_assignments': [assign.to_dict() for assign in
                                       all_assignments_flatten]}


@app.route('/schools/<int:school_id>')
def students_complete_percentile(school_id):
    all_students = Student.query.filter(Student.school_id == school_id).all()
    print(all_students)
    completed_assignments_counts = [student.completed_assignments for student
                                     in all_students]
    print(completed_assignments_counts)
    counts_greater_than_one = [count for count in completed_assignments_counts
                                if count > 1]
    print(counts_greater_than_one)
    if len(completed_assignments_counts) == 0:
        return "no student has completed assignments"
    percentile = len(counts_greater_than_one)/len(completed_assignments_counts)*100
    return {"Percentile Completed More Than One": percentile}
