from dotenv import load_dotenv
from app.models import db, Submission, Student, Course, Course_work, rosters
from app import app
from datetime import date

load_dotenv()


with app.app_context():
    db.drop_all()
    db.create_all()

    ian = Student(school_id=1, grade_level='first_grade')

    db.session.add(ian)


    s1 = Submission(course_work_id=1, course_id=1, student_id=1,
                    type="TURNED_IN", assigned_points=90.0,
                    max_points = 100.0)



    db.session.add(s1)

    # alissa.bookmarked_questions.append(q1)
    # angela.bookmarked_questions.append(q2)
    # db.session.add(alissa)
    # db.session.add(angela)

    c1 = Course(teacher_id=1, name = "algebra")
    c2 = Course(teacher_id=2, name = "geometry")
    c3 = Course(teacher_id=1, name = "literature")

    # t2.tagged_questions.append(q2)
    # t8.tagged_questions.append(q1)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)




    db.session.commit()
