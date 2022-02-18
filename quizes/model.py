import json
from random import sample, shuffle

class Card:

    def __init__(self, topic, question, answer, incorrect_answers):
        self.topic = topic
        self.question = question
        self.answer = answer
        self.answers = incorrect_answers + [answer]
        # shuffle the answers
        shuffle(self.answers)
    
    def transform_to_api_record(self):
        card = {
            "question": self.question,
            "answer": self.answer,
            "answers": self.answers
        }
        return card


class Api:

    def __init__(self, name):
        self.name = name
        with open(f"apis/{name}.json") as file:
            self.data = json.load(file)

    def save_api(self):
        with open(f"apis/{self.name}.json", "w") as file:
            return json.dump(self.data, file)

    def generate_quiz(self):
        quiz = [self.data[i] for i in sample(range(len(self.data)-1), 9)]
        return quiz

    def add_card(self, card):
        self.data.append(card.transform_to_api_record())


    def get_card_by_question(self, question):
        card = list(filter(lambda x: x['question'] == question, self.data))[0]
        return card



    def find_phrase(self, phrase):
        # this function is not used yet
        result = []
        for card in self.data:
            if phrase.lower() in str(card).lower():
                result.append(card)
        print(result)
        print(len(result))
        return result



#db_config = Api('db_config').data
# adsk = Api('system_administration')
# adsk.get_card_by_question('In file with extension ___ I\'m not expecting to find configuration data.')
# card = Card('a', 'b', 'c', 'd', 'e')
# card.answers

# adsk.find_phrase('SSH')
#new_question = {'question': 'Enjoy your food', 'answer': 'Smacznego'}
#adsk.db.append(new_question)
#adsk.save_db()
#adsk.db
