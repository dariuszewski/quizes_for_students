from distutils.command.config import config
from math import sin
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from forms import EditCardForm, NewCardForm
import json
import random
import ast
from model import Api, Card

app = Flask(__name__)
app.secret_key='secret'
bootstrap = Bootstrap5(app)

@app.route("/")
def welcome():
    return render_template(
        "welcome.html")


@app.route("/api/<topic>/")
def api(topic):
    return jsonify(Api(topic).data)


@app.route("/cards/<topic>/")
def cards(topic):
    session['topic'] = topic
    cards = Api(topic).data
    return render_template("cards.html", topic=topic, cards=cards)

@app.route("/edit_card/<question>", methods=["GET", "POST"])
def edit_card(question):

    if request.method == "POST":
        # flash(f'{form.data}')
        return redirect(url_for('welcome'))

    # set view values
    card = Api(session['topic']).get_card_by_question(question)
    
    incorrect_answers = list(filter(lambda x: x != card['answer'], card['answers']))
    form = EditCardForm(incorrect_answer_fields=incorrect_answers)

    form.topic.data = session['topic']
    form.question.data = card['question']
    form.answer.data = card['answer']

    # for i in range(len(incorrect_answers)):
    #     form.incorrect_answer_fields[i].data['default_value'] = incorrect_answers[i]

    return render_template(
            "edit_card.html", card=card, form=form, incorrect_answers=incorrect_answers
            )

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


        card = Card(request.form['topic'].replace(' ', '_').lower(), request.form['question'],
         request.form['answer'], request.form.getlist('incorrect_answer'))
        api = Api(request.form['topic'].replace(' ', '_').lower())

        api.add_card(card)
        api.save_api()

        flash(f'New card was successfully added to {api.name} dataset {card}.')
        return redirect(url_for('welcome'))

    form = NewCardForm()
    return render_template("add_card.html", form=form)


@app.route("/search", methods=["GET", "POST"])
def search(phrase=None):
    if request.method == "POST":
        phrase = request.form['question']
        result = Api('system_administration').find_phrase(phrase)

        return render_template("search.html", result=result)
    else:
        return render_template(
            "search.html")
