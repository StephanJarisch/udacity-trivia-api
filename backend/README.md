# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Make sure to make use of a virtual environment. To install conda check [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

Via Conda:

```bash
conda create --name trivia python=3.7 pip
conda activate trivia
```

If you have python3-venv installed:

```bash
python3 -m venv env
source env/bin/activate
```

As for your credentials create a .env file which contains the following information:

```bash
DB_NAME='*your-db-name*'
DB_TEST_NAME='*your-test-db-name*'
DB_USER='*your-db-username*'
DB_PASSWORD='*your-db-password*'
DB_HOST='*your-host:port*'
```

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

To run the server first declare two environment variables and finally run flask.

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Unit Test

To test the application run the shell script as follows:

```bash
sh test_flask.sh
```

## Documentation of Endpoints

### dictonary of categories

`GET '/categories'`

- no request arguments needed
- to test it in your local environment use:
    

```bash
curl -X GET http://127.0.0.1:5000/categories
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

`status code 200`

---

### list of questions

`GET '/questions'`

- no request arguments needed
- to test it in your local environment use:

```bash
curl -X GET http://127.0.0.1:5000/questions
```

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    "totalQuestions": 18,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

`status code 200`

---

### deleting a question

`DELETE '/questions/${id}'`

- pass the question {id} inside the url 
- to test it in your local environment use:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/1
```

```json
{
    "success": true
}
```

`status code 200`

---

### adding a question

`POST '/questions'`

- request arguments: "question" (string), "answer" (string), "difficulty" (int), "category" (int)
- to test it in your local environment use:
    'curl -X POST -d '{"question":"What's your name'?", "answer":"My name is Jeff", "difficulty":"1", "category":"1"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/questions'
'

```json
{
    "success": true
}
```

`status code 201`

---

### searching questions containing string

`POST '/searchTerm'`

- request argument: "searchTerm"
- to test it in your local environment use:

```bash
curl -X POST -d '{"searchTerm":"What"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/searchTerm
```

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    "totalQuestions": 1
}
```

`status code 200`

---

### questions from specific category

`POST '/categories/${id}/questions'`

- pass the category {id} in the url to get a subset of questions
- to test it in your local environment use:

```bash
curl -X POST http://127.0.0.1:5000/categories/1/questions
```

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    "totalQuestions": 1,
    "currentCategory": "Entertainment"
}
```

`status code 200`

---

### quiz backend

`POST '/quizzes'`

- returns a question 
- if previous questions (ids) are passed then they are excluded from the search pool
- required arguments: "previous_questions", "quiz_category"
- use "click" to get all topics
- to test it in your local environment use:
    
```bash
curl -X POST -d '{"previous_questions": [], "quiz_category":"click"}' -H "application/json" http://127.0.0.1:5000/quizzes
```

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    "totalQuestions": 1,
    "currentCategory": "Entertainment"
}
```
