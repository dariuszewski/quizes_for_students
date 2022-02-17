from distutils.command.config import config
from math import sin
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from forms import EditCardForm
import json
import random
import ast
from model import Api

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

@app.route("/edit_card/<single_card>", methods=["GET", "POST"])
def edit_card(single_card):

    # set view values
    card_dict = ast.literal_eval(single_card)
    incorrect_answers = list(filter(lambda x: x != card_dict['answer'], card_dict['answers']))

    form = EditCardForm(incorrect_answer_fields=incorrect_answers)
    
    form.question.data = card_dict['question']
    form.answer.data = card_dict['answer']

    iterator_incorrect_answers= iter(incorrect_answers)
    for i in range(len(form.incorrect_answer_fields)):
        form.incorrect_answer_fields[i].data['default_value'] = incorrect_answers[i]

    return render_template(
            "edit_card.html", topic=session['topic'], single_card=single_card, incorrect_answers=incorrect_answers, form=form)

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

        # create a list of all answers, exclude empty inputs, shuffle result.
        all_answers = list(filter(lambda x: x != "", 
                request.form.getlist('incorrect_answer') + [request.form['correct_answer']]
            ))
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

    db_config = Api('db_config').data
    return render_template("add_card.html", db_config=db_config)


@app.route("/search", methods=["GET", "POST"])
def search(phrase=None):
    if request.method == "POST":
        phrase = request.form['question']
        result = Api('system_administration').find_phrase(phrase)

        return render_template("search.html", result=result)
    else:
        return render_template(
            "search.html")

# @app.route("/test", methods=["GET", "POST"])
# def test():
#     form = MyForm()
#     return render_template(
#             "test.html", form=form)