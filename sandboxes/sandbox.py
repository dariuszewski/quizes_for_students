import json




import json


def load_db():
    with open("flashcards_db.json") as f:
        return json.load(f)

def save_db():
    with open("flashcards_db.json", "w") as f:
        return json.dump(db, f)

db = load_db()

from operator import index
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for


from model import DataBase

app = Flask(__name__)

counter = 0

@app.route("/")
def welcome():
    return render_template(
        "welcome.html",
        cards=db)

@app.route("/api/<topic>/")
def api_sysadm(topic):
    db = DataBase(topic)
    return jsonify(db)


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html", card=card, index=index, max_index=len(db)-1)
    except IndexError:
        abort(404)

@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}     
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:        
        return render_template("add_card.html")

@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:        
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    return jsonify(db)

@app.route("/api/card/<int:index>")
def api_card_view(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

'''
@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html", card=card, index=index, max_index=len(db)-1)
    except IndexError:
        abort(404)

@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}     
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:        
        return render_template("add_card.html")

@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:        
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_view(index):
    try:
        return db[index]
    except IndexError:
        abort(404)



                    <button>
                {% if index < max_index %}
                    <a href="{{ url_for('card_view', index=index + 1) }}">
                        Next card
                {% else %}
                    <a href="{{ url_for('card_view', index=0) }}">
                        Start over
                    </a>
                {% endif %}
            </button>
        </p>

        <a href="{{ url_for('remove_card', index=index) }}">Remove this card</a>
'''