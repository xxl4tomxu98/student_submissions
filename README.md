# Student Submission Dataset Building Connecting Server and Query Using Flask SqlAlchemy


## Schema of the Dataset
    Develop an API that can dynamically generate database queries:
    Group by student_id and count completed assignments
    Group by course_id and average grade
    Group by teacher_id and count assignments created
    Group by school_id and find percentage of students with more than 1 assignment completed

    Use the web framework of your choice. Also use the datastore of your choice, but we suggest simply using SQLite to get started. Imagine the following 3 datasets when executing queries:

    student_submission - this table describes all the assignments administered to students and their status
    submission_id (primary key)
    course_work_id
    course_id
    student_id
    status (enum NEW, TURNED_IN)
    assigned_points (float)
    max_points (float)

    roster - this table describes all the students rostered in a course
    student_id
    course_id

    student - this table describes additional information about a student
    student_id
    school
    grade_level

    course - this table describes additional information about a course
    teacher_id
    course_id
    name

    course_work - this table describes additional information about course work (assignments)
    course_id
    title
    due date

## Backend Setup and Process

- Database postgresql named "records" were created with owner "records_app" and password "password".

    ```sql
        create user records_app createdb password 'password';
    ```

    ```sql
        create database records with owner records_app;
    ```

- Within the service folder run

    ```bash
        pipenv shell
        python database.py
    ```

    Type of columns were specifically given, and PRIMARY KEYS and FOREIGN KEYS are defined.
    The id is PK for all the tables and student_id, course_id, and course_work_id are FKs for submissions table


## Flask App

- Since the tables are relational even though only five are present, For the sake of better query backend Flask sever are built to connect to the database using database handler psycopg2-binary and ORM SqlAlchemy to help fetching data as needed.

- .env and .flaskenv were created for environmental variables and entrypoint folder/files specification

- Implementation of the above Model schema were created with SqlAlchemy model against DB in file models.py

- Class functions were built around all tables to help facilitate querying in sqlAlchemy.

- Relationships based on foreign key were created to do this last step.

- There is an extra many to many table "roster" relationship built to represent relationship between students and courses tables.

- to_dict functions were built to facilitate sending JSON to frontend.

- I could draw a model schema on a chart to show relationships but believe this is not necessary since the schema is straightforward based table relations.

- In the file init.py within app folder the library dependencies were imported, connection to DB were setup and   initial flask app initiated.

- First, a Hello World index page were tested to see if Flask app works. it is on ```http://localhost:5000/```

- Then endpoint of routes for database query and filtering and calculations are carried out with helper functions.

- All the endpoints have been tested on backend browser ```http://localhost:5000/``` for all submissions, courses, course_works, students queries.

- Submission query based on specific id are also tested in the backend and worked well.

- Searches on submissions or course_works based on student_id, or course_id, teacher_id, and school_id filters are all tested successfully in the backend.

- For example, the output of the search json for student_id=1 on port 5000 are tested to work.

    ```http://localhost:5000/students/1```

- pipenv were were used to create isolated environment in service

    ``` pipenv install``` will install dependencies in the Pipfile

    ``` pipenv shell``` will activate the shell, then

    ``` flask run ``` will run the flask app
