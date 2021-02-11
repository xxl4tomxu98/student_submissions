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
    dean = Student(school_id=2, grade_level="third_grade")
    angela = Student(school_id=2, grade_level="fourth_grade")
    javier = Student(school_id=2, grade_level='second_grade')
    julie = Student(school_id=2, grade_level='fifth_grade')
    db.session.add(ian)
    db.session.add(alissa)
    db.session.add(dean)
    db.session.add(angela)
    db.session.add(javier)
    db.session.add(julie)

    c1 = Course(teacher_id=1, name = "algebra")
    c2 = Course(teacher_id=2, name = "geometry")
    c3 = Course(teacher_id=1, name = "literature")

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)

    alissa.enrolled_courses.append(c1)
    alissa.enrolled_courses.append(c3)
    ian.enrolled_courses.append(c2)
    ian.enrolled_courses.append(c1)
    javier.enrolled_courses.append(c1)
    julie.enrolled_courses.append(c3)
    dean.enrolled_courses.append(c2)
    angela.enrolled_courses.append(c1)
    julie.enrolled_courses.append(c1)
    dean.enrolled_courses.append(c3)
    db.session.add(alissa)
    db.session.add(ian)
    db.session.add(angela)
    db.session.add(julie)
    db.session.add(javier)
    db.session.add(dean)


    cw1 = Course_work(course_id=1, title="mid_term", due_date=date(2021, 3, 28))
    cw2 = Course_work(course_id=1, title="final_project", due_date=date(2021, 5, 25))
    cw3 = Course_work(course_id=2, title="quiz_1", due_date=date(2021, 2, 18))
    cw4 = Course_work(course_id=2, title="quiz_2", due_date=date(2021, 2, 28))
    cw5 = Course_work(course_id=3, title="mid_term", due_date=date(2021, 4, 1))
    cw6 = Course_work(course_id=3, title="quiz_1", due_date=date(2021, 2, 15))
    db.session.add(cw1)
    db.session.add(cw2)
    db.session.add(cw3)
    db.session.add(cw4)
    db.session.add(cw5)
    db.session.add(cw6)

    s1 = Submission(course_work_id=4, course_id=2, student_id=1,
                    type="TURNED_IN", assigned_points=90.0,
                    max_points = 100.0)
    s2 = Submission(course_work_id=3, course_id=2, student_id=1,
                    type="TURNED_IN", assigned_points=80.0,
                    max_points = 100.0)
    s3 = Submission(course_work_id=5, course_id=3, student_id=2,
                    type="NEW", assigned_points=0.0,
                    max_points = 100.0)
    s4 = Submission(course_work_id=1, course_id=1, student_id=2,
                    type="TURNED_IN", assigned_points=60.0,
                    max_points = 100.0)
    s5 = Submission(course_work_id=4, course_id=2, student_id=3,
                    type="TURNED_IN", assigned_points=70.0,
                    max_points = 100.0)
    s6 = Submission(course_work_id=2, course_id=1, student_id=4,
                    type="TURNED_IN", assigned_points=85.0,
                    max_points = 100.0)
    s7 = Submission(course_work_id=1, course_id=1, student_id=5,
                    type="NEW", assigned_points=0.0,
                    max_points = 100.0)
    s8 = Submission(course_work_id=2, course_id=1, student_id=6,
                    type="TURNED_IN", assigned_points=65.0,
                    max_points = 100.0)
    s9 = Submission(course_work_id=6, course_id=3, student_id=3,
                    type="NEW", assigned_points=0.0,
                    max_points = 100.0)
    s10 = Submission(course_work_id=5, course_id=3, student_id=6,
                    type="TURNED_IN", assigned_points=93.0,
                    max_points = 100.0)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(s6)
    db.session.add(s7)
    db.session.add(s8)
    db.session.add(s9)
    db.session.add(s10)

    db.session.commit()
