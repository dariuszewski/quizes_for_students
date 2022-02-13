from hmac import new
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, flash, session

import json
import random

from model import Api

app = Flask(__name__)

app.secret_key='secret'

@app.route("/")
def welcome():
    return render_template(
        "welcome.html")


@app.route("/api/<topic>/")
def api(topic):
    return jsonify(Api(topic).data)


@app.route("/cards/<topic>/")
def cards(topic):
    cards = Api(topic).data
    return render_template("cards.html", topic=topic, cards=cards)

@app.route("/quiz/<topic>/", methods=["GET", "POST"])
def quiz(topic):
    if request.method == "POST":
        # check quiz and return it as flash message
        quiz = session["quiz"]
        user_answers = request.form
        result = 0
        current_question = 0

        for question in quiz:
            if question['answer'] == user_answers[str(current_question)]: # some weird data structure here
                result += 1
            current_question += 1 

        topic_name = topic.replace('_', ' ').title()

        flash(f'Your result of {topic_name} quiz is {result}/9.')        
        return redirect(url_for('welcome'))


    quiz = Api(topic).generate_quiz()
    session['quiz'] = quiz
    return render_template("quiz.html", topic=topic, quiz=quiz)

@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":

        all_answers = [
            request.form['correct_answer'], 
            request.form['incorrect_answer1'], 
            request.form['incorrect_answer2'], 
            request.form['incorrect_answer3']
            ]
        random.shuffle(all_answers)

        new_card = {
            "question": request.form['question'],
            "answer": request.form['correct_answer'],
            "answers": all_answers
        }

        api = Api(request.form['topic'])
        api.data.append(new_card)
        api.save_api()
        flash(f'New card was successfully added to {api.name} dataset.')
        return redirect(url_for('welcome'))

    return render_template("add_card.html")


@app.route("/search", methods=["GET", "POST"])
def search(phrase=None):
    if request.method == "POST":
        phrase = request.form['question']
        result = Api('system_administration').find_phrase(phrase)

        return render_template("search.html", result=result)
    else:
        return render_template(
            "search.html")
