from models import *
import pandas as pd
import random
from __init__ import db
#from os.path import exists


class Leaderboard:

    def __init__(self):
        self.rankings = pd.DataFrame(
            columns=["Rank", "Team", "Model", "LID", "POS", "NER", "SA", "MT"])
        self.rankings = pd.read_csv('Rankings_store.csv')

    def get_scores(self):
        return_dict = self.rankings.to_dict('r')
        return return_dict

    def add_score(self, score):
        # ranking = pd.DataFrame(
        # columns=["Rank", "Team", "Model", "LID", "POS", "NER", "SA", "MT"])
        id, model_name, team_name, model_link, file_name, tasks = score.id, score.model, score.team, score.model_link, score.file_name, score.tasks
        new_rank = {"Rank": 1,
                    "Team": team_name,
                    "Model": model_name,
                    "LID": random.randint(1, 10),
                    "POS": random.randint(1, 10),
                    "NER": random.randint(1, 10),
                    "SA": random.randint(1, 10),
                    "MT": random.randint(1, 10)}

        self.rankings = self.rankings.append(new_rank, ignore_index=True)
        self.rankings.to_csv('Rankings_store.csv', index=False)

        for i in tasks:
            data = i(id=id, team=team_name, model=model_name,
                     link=model_link, rank=random.randint(1, 10))
            db.session.add(data)
        db.session.commit()
