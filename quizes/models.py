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
            
    def get_card_by_question(self, question_code):
        for card in self.data:
            if question_code == card['question'].lower().replace(' ', ''):
                return card
    
    def remove_card_by_question(self, question_code):
        for card in self.data:
            if question_code == card['question'].lower().replace(' ', ''):
                self.data.remove(card)

    def generate_quiz(self):
        quiz = [self.data[i] for i in sample(range(len(self.data)-1), 9)]
        return quiz

    def add_card(self, card):
        # this function is not used
        self.data.append(card.transform_to_api_record())

    def remove_card(self, card):
        # this function is not used
        self.data.remove(card.transform_to_api_record())





    def find_phrase(self, phrase):
        # this function is not used yet but is planned
        result = []
        for card in self.data:
            if phrase.lower() in str(card).lower():
                result.append(card)
        print(result)
        print(len(result))
        return result


class Database:

    def __init__(self):
        with open(f"apis/db_config.json") as file:
            self.data = json.load(file)

    @classmethod
    def get_api_codes(cls):
        codes = [api['code'] for api in Database().data]
        return codes
            
# db_config = Database()
# db_config.get_api_codes()
# db_config = Api('db_config').data
# adsk = Api('system_administration')
# card = adsk.get_card_by_question("second")
# card

#card.id == hash("To install Active Directory service in Windows Serwver, we need to configure ...")
# card = Card.from_api_record(adsk.name, c)
# card.question
# hash('In file with extension ___ I\'m not expecting to find configuration data.')
# adsk.find_phrase('SSH')
#new_question = {'question': 'Enjoy your food', 'answer': 'Smacznego'}
#adsk.db.append(new_question)
#adsk.save_db()
#adsk.db
