from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired
from models import Api


class CardForm(FlaskForm):
    topic = SelectField(label='Topic', choices=[dataset['dataset_title'] for dataset in Api('db_config').data], validators=[DataRequired()])
    question = TextAreaField(label="Question", validators=[DataRequired()])
    answer = StringField(label="Correct Answer", validators=[DataRequired()])
    incorrect_answer = StringField(label="Incorrect Answers", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

