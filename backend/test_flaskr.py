import os
import unittest
import json
import time
from urllib import response
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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_categories(self):
        """ TEST to get all categories """

        # check if the status code is correct
        res = self.client().get("/categories")
        self.assertEqual(res.status_code, 200)
        
        response_data = json.loads(res.get_data())
        
        # check if response contains 3 keys "success", "categories"
        self.assertEqual(len(list(response_data.keys())), 2)
        self.assertTrue("success" in list(response_data.keys()))
        self.assertTrue("categories" in list(response_data.keys()))

        # check if there are 6 values in the response (from dummy data)
        self.assertEqual(len(list(response_data["categories"])), 6)


    def test_all_questions(self):
        """ TEST to get all questions """

        # check if the status code is correct
        res = self.client().get("/questions?page=1")
        response_data = json.loads(res.get_data())

        # check status code
        self.assertEqual(res.status_code, 200)
        
        # check number of categories
        self.assertEqual(len(response_data["categories"]), 6)

        # check number of questions
        self.assertEqual(len(response_data["questions"]), 10)

        # check number of total questions
        self.assertEqual(response_data["totalQuestions"], 19)

    def test_delete_questions(self):
        """ TEST delete a question """

        # check if the status code is correct
        res = self.client().delete("/questions/2")
        
        # check status code
        self.assertEqual(res.status_code, 200)


        res = self.client().delete("/questions/1")
        # check status code
        self.assertEqual(res.status_code, 404)

        # check if there are just 18 questions left
        res = self.client().get("/questions?page=1")
        response_data = json.loads(res.get_data())
        self.assertEqual(response_data["totalQuestions"], 18)    

    def test_post_a_questions(self):
        """ TEST to post a question """

        # check if the status code is correct
        res = self.client().post("/questions", json={'question':'What is my name?', 'answer':'Jeff', 'difficulty':'1', 'category':'1'})
        response_data = json.loads(res.get_data())
        
        # check status code
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data["success"], True)

        
        # check if the status code is correct - MISSING "question"
        res = self.client().post("/questions", json={'answer':'Jeff', 'difficulty':'1', 'category':'1'})
        # check if the status code is correct - MISSING "answer"
        self.assertEqual(res.status_code, 400)
        res = self.client().post("/questions", json={'question':'What is my name?', 'difficulty':'1', 'category':'1'})
        # check if the status code is correct - MISSING "difficulty"
        self.assertEqual(res.status_code, 400)
        res = self.client().post("/questions", json={'question':'What is my name?', 'answer':'Jeff', 'category':'1'})
        self.assertEqual(res.status_code, 400)
        # check if the status code is correct - MISSING "category"
        res = self.client().post("/questions", json={'question':'What is my name?', 'answer':'Jeff', 'difficulty':'1'})
        self.assertEqual(res.status_code, 400)


        # check if there are 19 questions after adding question
        res = self.client().get("/questions?page=1")
        response_data = json.loads(res.get_data())
        self.assertEqual(response_data["totalQuestions"], 19)  

    def test_post_a_questions(self):
        """ TEST searching a question """

        # check if the status code is correct
        res = self.client().post("/searchTerm", json={'searchTerm':'what'})
        self.assertEqual(res.status_code, 200)

        response_data = json.loads(res.get_data())
        
        # check if success is True
        self.assertTrue(response_data["success"])

        # check if returned questions is the same as totalQuestions
        self.assertEqual(len(response_data["questions"]), 7)
        self.assertEqual(response_data["totalQuestions"], 7)

    def test_question_from_category(self):
        """ TEST questions from category """

        # check if the status code is correct
        res = self.client().get("/categories/1/questions")
        response_data = json.loads(res.get_data())
        self.assertEqual(res.status_code, 200)

        res = self.client().get("/categories/1000/questions")
        response_data = json.loads(res.get_data())

        # check if page 1000 returns 'page not found'
        self.assertEqual(res.status_code, 404)

    def test_question_for_quiz(self):
        """ TEST questions for quiz """

        # check if the status code is correct
        res = self.client().post("/quizzes", json={"previous_questions":[], "quiz_category": {"type": "History", "id": "3"}})
        self.assertEqual(res.status_code, 200)

        # missing input
        res = self.client().post("/quizzes")
        self.assertEqual(res.status_code, 400)

        res = self.client().post("/quizzes", json={"previous_questions":[], "quiz_category": {"type": "History", "id": "3"}})
        response_data = json.loads(res.get_data())

        # check if success key is returned
        self.assertTrue(response_data["success"])

        # check if question is returned as dict
        self.assertTrue(isinstance(response_data["question"], dict))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()