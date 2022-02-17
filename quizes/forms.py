from ast import Sub
from cProfile import label
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, TextAreaField, StringField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired
from model import Api

class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])

class IncorrectAnsewrForm(FlaskForm):
    incorrect_answer = StringField()


class EditCardForm(FlaskForm):
    topic = SelectField(label='Topic', choices=[dataset['dataset_title'] for dataset in Api('db_config').data], validators=[DataRequired()])
    question = TextAreaField(label="Question", validators=[DataRequired()])
    answer = StringField(label="Correct Answer", validators=[DataRequired()])
    incorrect_answer_fields= FieldList(FormField(IncorrectAnsewrForm), min_entries=1)
    update = SubmitField(label="Update")
    delete = SubmitField(label="Delete")
