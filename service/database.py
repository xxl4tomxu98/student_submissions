from dotenv import load_dotenv
from app.models import db, Submission, Student, Course, Course_work, rosters
from app import app
from datetime import date

load_dotenv()


with app.app_context():
    db.drop_all()
    db.create_all()

    ian = Student(school_id=1, grade_level='first_grade')
    alissa = Student(school_id=2, grade_level='second_grade')
    db.session.add(ian)
    db.session.add(alissa)

    c1 = Course(teacher_id=1, name = "algebra")
    c2 = Course(teacher_id=2, name = "geometry")
    c3 = Course(teacher_id=1, name = "literature")

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)

    alissa.enrolled_courses.append(c1)
    alissa.enrolled_courses.append(c3)
    ian.enrolled_courses.append(c2)
    db.session.add(alissa)
    db.session.add(ian)

    cw1 = Course_work(course_id=1, title="mid_term")
    cw2 = Course_work(course_id=1, title="final_project")
    cw3 = Course_work(course_id=2, title="quiz_1")
    cw4 = Course_work(course_id=2, title="quiz_2")
    cw5 = Course_work(course_id=3, title="mid_term")
    cw6 = Course_work(course_id=3, title="quiz_1")
    db.session.add(cw1)
    db.session.add(cw2)
    db.session.add(cw3)
    db.session.add(cw4)
    db.session.add(cw5)
    db.session.add(cw6)

    s1 = Submission(course_work_id=1, course_id=1, student_id=1,
                    type="TURNED_IN", assigned_points=90.0,
                    max_points = 100.0)
    s2 = Submission(course_work_id=1, course_id=2, student_id=1,
                    type="TURNED_IN", assigned_points=80.0,
                    max_points = 100.0)
    s3 = Submission(course_work_id=2, course_id=3, student_id=2,
                    type="NEW", assigned_points=0.0,
                    max_points = 100.0)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)




    db.session.add(s1)


    db.session.commit()
