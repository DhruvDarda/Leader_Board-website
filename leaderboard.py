from models import *
import pandas as pd
import random
from __init__ import db
#from os.path import exists


class Leaderboard:

    def __init__(self):
        pass

    def add_score(self, score):
        # ranking = pd.DataFrame(
        # columns=["Rank", "Team", "Model", "LID", "POS", "NER", "SA", "MT"])
        id, model_name, team_name, model_link, file_name, tasks = score.id, score.model, score.team, score.model_link, score.file_name, score.tasks

        '''funcs = {'LID': LID, 'NER': NER, 'POS': POS, 'SA': SA, 'MT': MT}
        for i in tasks:
            data = funcs[i](id=id, team=team_name, model=model_name,
                            link=model_link, rank=random.randint(1, 10))
            db.session.add(data)
        db.session.commit()
        '''
        funcs = {'LID': -1, 'NER': -1, 'POS': -1, 'SA': -1, 'MT': -1}
        for i in tasks:
            funcs[i] = 1
        data = Leaderboard_CM(id=id, team=team_name, model=model_name,
                              link=model_link, rank=random.randint(1, 10), lid=funcs['LID'], pos=funcs['POS'], ner=funcs['NER'], sa=funcs['SA'], mt=funcs['MT'])
        db.session.add(data)
        db.session.commit()
