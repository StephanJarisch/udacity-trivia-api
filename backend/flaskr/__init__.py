import json
import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import null, true

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            # get categories ordered as dict
            categories_query = Category.query.order_by(Category.id).all()
            categories = {
                elem.id: elem.type for elem in categories_query
            }

            return jsonify({
                "success": True,
                "categories": categories
            }), 200

        except Exception as e:
            abort(500)

        finally:
            db.session.close()

    @app.route("/questions", methods=["GET"])
    def get_all_questions():
        try:
            # get argument
            page = request.args.get('page', 1, type=int)

            # start and end of pagination
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            # get questions in the right format
            questions_query = Question.query.order_by(Question.id).all()
            questions = [question.format() for question in questions_query]

            # get categories
            categories_query = Category.query.order_by(Category.id).all()
            categories = {
                elem.id: elem.type for elem in categories_query
            }
            if len(questions[start:end]) == 0:
                return jsonify(custom_abort(404)), 404

            return jsonify({
                "success": True,
                "questions": questions[start:end],
                "totalQuestions": len(questions),
                "categories": categories
            })

        except Exception as e:
            abort(500)

        finally:
            db.session.close()

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        try:
            # get question which to delete
            question_to_delete = db.session.query(Question).filter(
                Question.id == question_id
            ).one_or_none()

            # abort with 'page not found' if question is not found
            if question_to_delete is None:
                return jsonify(custom_abort(404)), 404

            # delete question
            question_to_delete.delete()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            # check if user sent an json object
            if request.json is None:
                return jsonify(custom_abort(400)), 400

            # check if required elements in request
            for elem in ["question", "answer", "difficulty", "category"]:
                if elem not in request.json.keys():
                    return jsonify(custom_abort(400)), 400

            # insert new Question
            new_question = Question(
                request.json["question"],
                request.json["answer"],
                request.json["category"],
                request.json["difficulty"]
            )
            new_question.insert()

            return jsonify({
                "success": True
            }), 201

        except Exception as e:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route("/searchTerm", methods=["POST"])
    def question_from_search_term():
        try:
            # check if user sent an json object
            if request.json is None:
                return jsonify(custom_abort(400)), 400

            # check if required elements in request
            for elem in ["searchTerm"]:
                if elem not in request.json.keys():
                    return jsonify(custom_abort(400)), 400

            # get questions like the search term
            questions_query = Question.query.filter(
                Question.question.ilike('%' + request.json["searchTerm"] + '%')
            ).all()
            questions = [question.format() for question in questions_query]

            if len(questions) == 0:
                return jsonify(custom_abort(404)), 404

            return jsonify({
                "success": True,
                "questions": questions,
                "totalQuestions": len(questions)
            }), 200

        except Exception as e:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def question_from_category(category_id):
        try:
            # get questions of a specific category
            questions_query = Question.query.order_by(
                Question.id
            ).filter(Question.category == category_id).all()
            questions = [question.format() for question in questions_query]

            # get categories to return 'currentCategory'
            categories_query = Category.query.order_by(Category.id).all()
            categories = {
                elem.id: elem.type for elem in categories_query
            }

            # if category is not found abort
            if category_id not in categories.keys():
                return jsonify(custom_abort(404)), 404

            return jsonify({
                "success": True,
                "questions": questions,
                "totalQuestions": len(questions),
                "currentCategory": categories[category_id]
            }), 200

        except Exception as e:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route("/quizzes", methods=["POST"])
    def question_for_quiz():
        try:
            # check user input is json object
            if request.json is None:
                return jsonify(custom_abort(400)), 400

            # check if required elements in request
            for elem in ["previous_questions", "quiz_category"]:
                if elem not in request.json.keys():
                    return jsonify(custom_abort(400)), 400

            # get questions of user chosen category
            category = request.json["quiz_category"]["id"]
            if category == 0:
                questions_query = Question.query.all()
            else:
                questions_query = Question.query.filter(
                    Question.category == category
                ).all()
            questions = [
                question.format()
                for question in questions_query
                if question.id not in request.json["previous_questions"]
            ]

            # if no questions left or found return just success
            if len(questions) == 0:
                return jsonify(custom_abort(404)), 404

            # otherwise return single question
            random_index = random.randint(0, len(questions)-1)
            return jsonify({
                "success": True,
                "question": questions[random_index],
            }), 200

        except Exception as e:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    def custom_abort(value: 404):
        # CUSTOM ERROR HANDLER - BECAUSE
        # inside a try - except statement flask-abort does not work!!
        if value == 400:
            return {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        if value == 404:
            return {
                "success": False,
                "error": 404,
                "message": "Not found"
            }

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "not processable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    return app
