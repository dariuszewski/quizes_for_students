from flask import Flask, render_template, abort, jsonify, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from forms import CardForm
import json
import random
import ast
from models import Database, Api

app = Flask(__name__)
app.secret_key='secret'
bootstrap = Bootstrap5(app)

@app.route("/")
def welcome():

    return render_template("welcome.html", db=Database().data)

@app.route("/test/")
def test():

    return render_template("test.html")

@app.route("/api/<topic>/")
def api(topic):

    return jsonify(Api(topic).data)



@app.route("/cards/<topic>/")
def cards(topic):

    session['topic'] = topic
    cards = Api(topic).data
    for card in cards:
        card['question_code'] = card['question'].lower().replace(' ', '')
    return render_template("cards.html", topic=topic, cards=cards)


@app.route("/card/<question_code>")
def card(question_code):

    api = Api(session['topic'])
    card = api.get_card_by_question(question_code)
    return render_template("card.html", card=card, question_code=question_code)

@app.route("/delete_card/<question_code>")
def delete_card(question_code):

        api = Api(session['topic'])
        api.remove_card_by_question(question_code)
        api.save_api()
        flash('Selected card was successfully deleted.')
        return redirect(url_for('cards', topic=session['topic'], question_code=question_code))


@app.route("/add_card", methods=["GET", "POST"])
def add_card():

    form = CardForm()

    if form.validate_on_submit():

        api = Api(request.form['topic'].replace(' ', '_').lower())
        new_card = {
            "question": request.form['question'],
            "answer": request.form['answer'],
            "answers": request.form.getlist('incorrect_answer') + [request.form['answer']]
        }

        api.data.append(new_card)
        api.save_api()

        flash(f'New card was successfully added to {api.name} dataset {card}.', 'success')
        return redirect(url_for('welcome'))

    
    return render_template("add_card.html", form=form)


@app.route("/update_card/<question_code>", methods=["GET", "POST"])
def update_card(question_code):

    api = Api(session['topic'])
    card = api.get_card_by_question(question_code)
    form = CardForm()

    if request.method == "POST":
        # delte old version
        api.remove_card_by_question(question_code)
        api.save_api()
        # save new version
        api = Api(request.form['topic'].replace(' ', '_').lower())
        new_card = {
            "question": request.form['question'],
            "answer": request.form['answer'],
            "answers": request.form.getlist('incorrect_answer') + [request.form['answer']]
        }

        api.data.append(new_card)
        api.save_api()

        flash(f"Card was successfully updated.")
        return redirect(url_for('welcome'))

    form.topic.data = api.name
    form.question.data = card['question']
    form.answer.data = card['answer']
    invalid_answers =  list(filter(lambda x: x != card['answer'], card['answers']))

    return render_template("update_card.html", card=card, question_code=question_code, form=form, invalid_answers=invalid_answers)


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



@app.route("/search", methods=["GET", "POST"])
def search(phrase=None):
    if request.method == "POST":
        phrase = request.form['question']
        result = Api('system_administration').find_phrase(phrase)

        return render_template("search.html", result=result)
    else:
        return render_template(
            "search.html")
