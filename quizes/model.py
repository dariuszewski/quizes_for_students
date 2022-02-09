import json


class Api:

    def __init__(self, name):
        self.name = name
        with open(f"apis/{name}.json") as file:
            self.data = json.load(file)

    def save_db(self):
        with open(f"apis/{self.name}.json", "w") as file:
            return json.dump(self.data, file)


#adsk = Entity('system_administration')
#new_question = {'question': 'Enjoy your food', 'answer': 'Smacznego'}
#adsk.db.append(new_question)
#adsk.save_db()
#adsk.db
