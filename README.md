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
  -- The id is PK for submissions table


## Flask App
- Since the tables are relational even though only five are present, For the sake of better query backend Flask sever are built to connect to the database using database handler psycopg2-binary and ORM SqlAlchemy to help fetching data as needed.

- .env and .flaskenv were created for environmental variables and entrypoint folder/files specification

- Model schema were created with SqlAlchemy model against DB in file models.py

  --class functions were built especially around submissions table to help facilitate querying in sqlAlchemy.

  --relationships based on foreign key were created to do this last step.

  --there is an extra many to many table "roster" relationship built for the sake of if user wants to add more tags to movies and is NOT used in this query excercise.

  --to_dict functions were built to facilitate sending JSON to frontend. But need "MyJSONEncoder" class to help encoding problems with columns of Numeric values.

  --I could draw a model schema on a chart to show relationships but believe this is not necessary since the schema is straightforward based table relations.

- In the file init.py within app folder the library dependencies were imported, connection to DB were setup and     initial flask app initiated. Please see detailed comments in the files for further reference.

- First, a Hello World index page were tested to see if Flask app works. it is on ```http://localhost:5000/```

- Then endpoint of routes for database query and filtering and calculations are carried out with helper functions.

- All the endpoints have been tested on backend browser ```http://localhost:5000/``` for all movies, tags, ratings, links queries.

- Movie query based on specific movie_id are also tested in the backend and worked well.

- Searches on movies based on movies column names, or tag, rating, and user filters are all tested successfully in the backend.

- For example, the output of the search json for movie_id=3000 on port 5000 are tested to work. ```http://localhost:5000/movies/3000```

  -- pipenv were were used to create isolated environment in service

  ``` pipenv install``` will install dependencies in the Pipfile

  ``` pipenv shell``` will activate the shell, then

  ``` flask run ``` will run the flask app

## Fronend React App

- ```npm install``` will install dependencies

- ```npm start``` will run the react app

- key Ajax code that fetch flask endpoint json dataset can be seen as below:
``` searchMovies = async () => {
    const term = this.state.term;
    const res = await fetch(`/search/${term}`)
    if (res.ok) {
        const { list } = await res.json();
        console.log(list)
        this.setState({
          movieData: list,
        })
        return list;
    }
    throw res;
  }
```
- UI design is such that all four major fronend queries are listed side by side horizontally to save space.

- Four forms and buttons were created to do:

  -- Group by student_id and count completed assignments,

  -- Group by course_id and average grade,

  -- Group by teacher_id and count assignments created,

  -- Group by school_id and find percentage of students with more than 1 assignment completed.

- Paginations are designed in component "SearchDB.js" so that buttons of all possible pages are listed in the page and each page contains 3 movies due to limitations on space each page. The data were sorted starting most recent released movies first and going back in years.



# Cross Origin Resourse Sharing
- CORS issue has to be addressed because I am rendering on port 8000 from data from port 5000
  -- the code to prevent CORS porblem is to have the following proxy declaration in client/package.json.

  ``` "proxy": "http://localhost:5000" ```
