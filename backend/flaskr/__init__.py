import os
from flask import Flask, request, abort, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request , selection):
  page = request.args.get('page' , 1 , type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors= CORS(app , resources= {r"/*":{"origins":"*"}})

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers' , 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods' , 'GET,POST,PATCH,DELETE,OPTIONS')
    return response 
    
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.route('/categories')
  def retrieve_categories():
    #get all categories
    categories = Category.query.order_by(Category.id).all()

    if len(categories) == 0:
      abort(404)
    #formatting categories
    categories_response = {category.id : category.type for category in categories}

    return jsonify({
      'success':True ,
      'categories':categories_response,
      'total_categories':len(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/questions')
  def retrieve_questions():
    #get all questions
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request , selection)
    #get all categories
    categories = Category.query.order_by(Category.id).all()
    categories_response = {category.id : category.type for category in categories}

    if len(current_questions) == 0 or len(categories) == 0 :
      abort(404)
      
    return jsonify({
      'success':True , 
      'questions':current_questions,
      'total_questions':len(selection),
      'current_category':None ,
      'categories': categories_response
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions/<int:question_id>' , methods=['DELETE'])
  def delete_question_by_id(question_id):
    #get the deleted question id
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None :
      abort(404)

    try:
      #deleting the question
      question.delete()
      return jsonify({
        'success':True ,
        'deleted':question_id
      })
    
    except:
      abort(422)
    
    
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions' , methods=['POST'])
  def create_question():
    #getting the whole request data
    data = request.get_json()
    #getting each request object
    question=data.get('question' , None)
    answer =data.get('answer' , None)
    category=data.get('category' , None)
    difficulty=data.get('difficulty' , None)
    search_term= data.get('searchTerm' , None)

    try:
      #If the request contains searchTerm then its search request otherwise its a create request
      if search_term is not None:
        #getting the results case insensitive
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
        current_questions = paginate_questions(request , selection)

        return jsonify({
          'success':True ,
          'questions':current_questions,
          'total_questions': len(selection)
        })

      else:
        new_question = Question(
          question=question, 
          answer=answer,
          category=category,
          difficulty=difficulty
          )
        new_question.insert()

        return jsonify({
          'success':True ,
          'created':new_question.id
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_category_questions(category_id):
    try:
      #Getting questions based on their categories
      selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
      current_questions= paginate_questions(request , selection)
      if len(selection)==0:
        abort(404)
      return jsonify({
        'success':True ,
        'questions':current_questions  ,
        'total_questions':len(selection)
      })
    
    except :
      abort(422)


    

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/quizzes' , methods=['POST'])
  def play_game():
    #getting the request data
    quiz_category= request.get_json().get('quiz_category',None)
    previous_questions= request.get_json().get('previous_questions',None)

    if quiz_category is None or previous_questions is None :
      abort(400)
    #if quiz id is 0 then get a question from all categories that's id doesn't exist in previous_questions
    #else do same thing but within given category
    if quiz_category['id'] == 0:
      questions= Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:
      questions= Question.query.filter(Question.id.notin_(previous_questions)).filter(Question.category == quiz_category['id']).all()

    if len(questions)==0:
      question = None 
    else:
      question = questions[random.randrange(0,len(questions),1)].format()

    return jsonify({
      'success':True ,
      'question': question
    })      
   



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False ,
      'error':404 ,
      'message' : 'resource not found'
    }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False , 
      'error': 422 ,
      'message': 'unprocessable'
    }),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False , 
      'error':400 ,
      'message': 'bad request'
    }),400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'error':405 ,
      'message':'method not allowed'
    }),405
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    