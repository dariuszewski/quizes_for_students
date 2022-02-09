from operator import index
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for


from model import Api

app = Flask(__name__)

counter = 0

@app.route("/")
def welcome():
    return render_template(
        "welcome.html")


@app.route("/api/<topic>/")
def api(topic):
    return jsonify(Api(topic).data)

