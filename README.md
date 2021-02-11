## Backend Setup and Process

  -- Database postgresql named "records" were created with owner "records_app" and password "password".

     ```create user records_app createdb password 'password'; ```

     ```create database records with owner records_app; ```

  -- Within the service folder run
     ```
        pipenv shell

        python database.py
     ```

  -- Type of columns were specifically given, and PRIMARY KEYS and FOREIGN KEYS are defined.
  -- The id is PK for all the tables and student_id, course_id, and course_work_id are FKs for submissions table


## Flask App
- Since the tables are relational even though only five are present, For the sake of better query backend Flask sever are built to connect to the database using database handler psycopg2-binary and ORM SqlAlchemy to help fetching data as needed.

- .env and .flaskenv were created for environmental variables and entrypoint folder/files specification

- Model schema were created with SqlAlchemy model against DB in file models.py

  --class functions were built around all tables to help facilitate querying in sqlAlchemy.

  --relationships based on foreign key were created to do this last step.

  --there is an extra many to many table "roster" relationship built to represent relationship between students and courses tables.

  --to_dict functions were built to facilitate sending JSON to frontend.

  --I could draw a model schema on a chart to show relationships but believe this is not necessary since the schema is straightforward based table relations.

- In the file init.py within app folder the library dependencies were imported, connection to DB were setup and     initial flask app initiated.

- First, a Hello World index page were tested to see if Flask app works. it is on ```http://localhost:5000/```

- Then endpoint of routes for database query and filtering and calculations are carried out with helper functions.

- All the endpoints have been tested on backend browser ```http://localhost:5000/``` for all submissions, courses, course_works, students queries.

- Submission query based on specific id are also tested in the backend and worked well.

- Searches on submissions or course_works based on student_id, or course_id, teacher_id, and school_id filters are all tested successfully in the backend.

- For example, the output of the search json for student_id=1 on port 5000 are tested to work. ```http://localhost:5000/students/1```

  -- pipenv were were used to create isolated environment in service

  ``` pipenv install``` will install dependencies in the Pipfile

  ``` pipenv shell``` will activate the shell, then

  ``` flask run ``` will run the flask app
