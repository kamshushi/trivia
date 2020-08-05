# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

- Sample request and response :
Request: curl localhost:5000/categories
Response:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/questions?page=value'
- Fetches all questions in the current page based on the query parameters provided
in the request(page=value) which default page is 1 if no parameters provided and  also fetches all categories
-Request Arguments : page=value query parameters 

-Sample request and response:
Request: curl localhost:5000/questions?page=2
Response:
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "A New Answer",
      "category": 6,
      "difficulty": 3,
      "id": 24,
      "question": "A New Question ?"
    }
  ],
  "success": true,
  "total_questions": 19
}


DELETE '/questions/<int:question_id>'
- Deletes a question by the given id 
- Request Arguments : question_id 

- Sample Request and Response:
Requset: curl -X DELETE localhost:5000/questions/10
Response:
{
  "deleted": 10,
  "success": true
}


POST '/questions' 
-Either create a new question or search for questions by keyword (case insensitive), depending on the request arguments.
-Request Arguments to CREATE a new question :
{
    'question':'When was the band Guns N Roses formed ?',
    'answer':'1985',
    'category':2,
    'difficulty':3
}
-Request Arguments to SEARCH for questions by keyword :
{
    'searchTerm':'When'
}

- Sample Request and Response to CREATE a new question :
Request: curl -X POST -H "Content-Type:application/json" localhost:5000/questions -d '{"question":"When was the band Guns N Roses formed ?" , "answer":"1985" , "category":2 , "difficulty":3}'

Response:
{
  "created": 27,
  "success": true
}

- Sample Request and Response to SEARCH for questions by keyword
Request:
curl -X POST -H "Content-Type:application/json" localhost:5000/questions -d '{"searchTerm":"When"}'
Response:
{
  "questions": [
    {
      "answer": "1985",
      "category": 2,
      "difficulty": 3,
      "id": 27,
      "question": "When was the band Guns N Roses formed ?"
    }
  ],
  "success": true,
  "total_questions": 1
}


GET '/categories/<int:category_id>/questions'
-Fetches all questions of the current category in the url 
-Request Arguments : None 

- Sample Request , Response :
Request: curl localhost:5000/categories/2/questions
Response:
{
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "1985",
      "category": 2,
      "difficulty": 3,
      "id": 27,
      "question": "When was the band Guns N Roses formed ?"
    }
  ],
  "success": true,
  "total_questions": 5
}


POST '/quizzes' 
-Fetches a random question within the given category and it's not in the previous questions
-Request Arguments: {
    'quiz_category': {'id':value , 'category':value}
    'previous_questions': [list of integer values(questions ids)]
}

-Sample Request and Response:
Request: curl -X POST -H "Content-Type:application/json" localhost:5000/quizzes -d '{"quiz_category":{"id":2 , "category":"Art"} , "previous_questions":[16,17,18]}'
Response:
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```