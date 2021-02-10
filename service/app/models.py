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
    # student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    type = db.Column(db.Enum("NEW", "TURNED_IN", name="status"))
    assigned_points = db.Column(db.Float, nullable=False)
    max_points = db.Column(db.Float, nullable=False)




    @property
    def all_tags(self):
        tags = Tag.query.filter_by(movie_id=self.movie_id).all()
        return [t.tag for t in tags]

    @property
    def imdb_tmdb(self):
        movie = Link.query.filter_by(movie_id=self.movie_id).first()
        return (movie.imdb_id, movie.tmdb_id)

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "genres": self.genres_array,
            "release_year": self.release_year,
            "tag_count": self.tag_count,
            "all_tags": self.all_tags,
            "rating_count": self.rating_count,
            "avg_rating": self.avg_rating,
            "imdb_tmdb": self.imdb_tmdb,
        }


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    grade_level = db.Column(db.String(255), nullable=False)

    # student_submissions = db.relationship('Submission',
    #                                       backref='student', lazy=True)
    enrolled_courses = db.relationship('Course',
                                       back_populates='signedup_students',
                                       secondary='rosters')

    @property
    def completed_assigment_count(self):
        all_courses = self.enrolled_courses
        all_assignments = [work for work in course.course_works for
                           course in all_courses]
        return len([assignment for assignment in all_assignments
                    if assignment.type = 'TURNED_IN'])

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "grade_level": self.grade_level,
            "enrolled_courses": self.enrolled_courses,
            "completed_assigment_count": self.completed_assigment_count,
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
    def avg_grade(self):
        ratings = Rating.query.filter_by(movie_id=self.movie_id).all()
        all_ratings = [r.rating for r in ratings]
        if len(all_ratings) != 0:
            return "{:2.1f}".format(sum(all_ratings)/len(all_ratings))
        return 0

    def to_dict(self):
        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "name": self.name,
        }


class Course_work(db.Model):
    __tablename__ = "course_works"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    work_submissions = db.relationship('Submission', backref='course_work', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "due_date": self.due_date,
        }

# def decimal_default(obj):
#     if isinstance(obj, decimal.Decimal):
#         return float(obj)
#     raise TypeError
