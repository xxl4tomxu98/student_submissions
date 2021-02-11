from flask_sqlalchemy import SQLAlchemy
import flask.json, decimal
from datetime import datetime

db = SQLAlchemy()


rosters = db.Table(
    'rosters',
    db.Model.metadata,
    db.Column(
        'student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True
    ), db.Column('course_id', db.Integer,
                 db.ForeignKey('courses.id'), primary_key=True)
)


# This is flask json encoding for jsonify Numeric object like rating
# class MyJSONEncoder(flask.json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             # Convert decimal instances to strings.
#             return str(obj)
#         return super(MyJSONEncoder, self).default(obj)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    course_work_id = db.Column(db.Integer, db.ForeignKey('course_works.id'),
                               nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    type = db.Column(db.Enum("NEW", "TURNED_IN", name="status"))
    assigned_points = db.Column(db.Float, nullable=False)
    max_points = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "course_work_id": self.course_work_id,
            "course_id": self.course_id,
            "student_id": self.student_id,
            "status": self.type,
            "assigned_points": self.assigned_points,
            "max_points": self.max_points,
        }


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    grade_level = db.Column(db.String(255), nullable=False)
    student_submissions = db.relationship('Submission',
                                           backref='student', lazy=True)
    enrolled_courses = db.relationship('Course',
                                       back_populates='signedup_students',
                                       secondary='rosters')

    @property
    def total_submissions(self):
        return len(self.student_submissions)

    @property
    def total_enrolled_courses(self):
        return len(self.enrolled_courses)

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "grade_level": self.grade_level,
            "total_enrolled_courses": self.total_enrolled_courses,
            "total_submissions": self.total_submissions,
        }


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))

    course_submissions = db.relationship('Submission', backref='course', lazy=True)
    course_works = db.relationship('Course_work', backref='course', lazy=True)
    signedup_students = db.relationship('Student',
                                       back_populates='enrolled_courses',
                                       secondary='rosters')
    @property
    def submissions_count(self):
        return len(self.course_submissions)

    @property
    def assignments_count(self):
        return len(self.course_works)

    @property
    def enrolled_students_count(self):
        return len(self.signedup_students)

    def to_dict(self):
        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "name": self.name,
            "submissions_count": self.submissions_count,
            "assignments_count": self.assignments_count,
            "enrolled_students_count": self.enrolled_students_count,
        }


class Course_work(db.Model):
    __tablename__ = "course_works"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    work_submissions = db.relationship('Submission', backref='course_work', lazy=True)

    @property
    def count_all_submissions(self):
        all_submissions = self.work_submissions
        return len(all_submissions)


    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "due_date": self.due_date,
            "submissions_count": self.count_all_submissions,
        }

# def decimal_default(obj):
#     if isinstance(obj, decimal.Decimal):
#         return float(obj)
#     raise TypeError
