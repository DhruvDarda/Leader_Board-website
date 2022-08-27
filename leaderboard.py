from models import Score
import pandas as pd
import random
#from os.path import exists
#import os


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
        id, model_name, team_name, model_link, file_name = score.id, score.model, score.team, score.model_link, score.file_name
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
