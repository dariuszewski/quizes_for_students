import json
from random import sample

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

    def find_phrase(self, phrase):
        # this function is not used yet
        result = []
        for card in self.data:
            if phrase.lower() in str(card).lower():
                result.append(card)
        print(result)
        print(len(result))
        return result




# adsk = Api('system_administration')
# adsk.generate_quiz()
# adsk.find_phrase('SSH')
#new_question = {'question': 'Enjoy your food', 'answer': 'Smacznego'}
#adsk.db.append(new_question)
#adsk.save_db()
#adsk.db
