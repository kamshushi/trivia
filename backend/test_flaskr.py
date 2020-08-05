import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:123@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        #new question for testing POST '/questions'
        self.new_question={
            'question':'Is this the new question for testing ?',
            'answer':'Yes, this is the new question for testing ',
            'category':3,
            'difficulty':1
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data= json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_404_category_not_found(self):
        res= self.client().get('/categories')
        data=json.loads(res.data)
        if data['total_categories'] == 0:
            self.assertEqual(res.status_code , 404)
            self.assertEqual(data['success'] , False)
            self.assertEqual(data['message'] , 'resource not found')

    def test_get_questions(self):
        res=self.client().get('/questions')
        data= json.loads(res.data) 

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'] , None)
        self.assertTrue(data['categories'])

    def test_404_get_non_existent_questions(self):
        res=self.client().get('/questions?page=10000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'resource not found')
    
    def test_delete_question_by_id(self):
        res= self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertEqual(data['deleted'], 5)

    def test_404_delete_non_existent_question(self):
        res= self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'] , False)
        self.assertEqual(data['message'] , 'resource not found')

    def test_create_new_question(self):
        res=self.client().post('/questions' , json=self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)    
        self.assertTrue(data['created'])

    def test_405_creation_not_allowed(self):
        res= self.client().post('/questions/5' , json=self.new_question)
        data=json.loads(res.data) 

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'] , False)
        self.assertEqual(data['message'] , 'method not allowed')
        
    
    def test_search_for_questions_by_keyword_with_results(self):
        res= self.client().post('/questions' , json={'searchTerm':'wHaT'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertEqual(len(data['questions']) ,8)
        self.assertEqual(data['total_questions'],8)

    def test_200_no_search_results(self):
        res= self.client().post('/questions' , json={'searchTerm':'football'})
        data= json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertEqual(len(data['questions']) , 0)
        self.assertEqual(data['total_questions'] , 0)

    def test_get_questions_by_category(self):
        res= self.client().get('/categories/1/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertEqual(len(data['questions']) , 3)
        self.assertEqual(data['total_questions'],3)

    def test_422_questions_not_found_in_this_category(self):
        res= self.client().get('/categories/10000/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code , 422) 
        self.assertEqual(data['success'] , False) 
        self.assertEqual(data['message'] , 'unprocessable')

    

    #Testing playing the game by sending previous questions and category , knowing that
    #the returned question id must be 19 as it will be the last question of this category
    def test_play_game(self):
        res= self.client().post('/quizzes' , json={
            'previous_questions':[16,17,18] ,
            'quiz_category':{'type':'Art' , 'id':'2'}
             })
        data= json.loads(res.data) 

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['question']['id'] , 19)

    def test_400_play_game_where_data_is_none(self):
        res= self.client().post('/quizzes' , json={})
        data= json.loads(res.data) 

        self.assertEqual(res.status_code , 400)
        self.assertEqual(data['success'] , False)
        self.assertEqual(data['message'],'bad request')
        
        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()