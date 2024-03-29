from django.apps import AppConfig
import numpy as np
import os

boards = []


def setup_ques(name):
    global boards
    quizzes = np.zeros((1000000, 81), np.int32)
    
    with open(f'./{name}/static/sudoku.csv', 'r') as file:
        next(file)  # Skip the header line
        for i, line in enumerate(file):
            if "," in line:
                quiz, solution = line.strip().split(",")
                for j, q_s in enumerate(zip(quiz, solution)):
                    q, s = q_s
                    quizzes[i, j] = q

    boards = quizzes.reshape((-1, 9, 9))

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self) -> None:
        if os.environ.get('RUN_MAIN'):setup_ques(self.name)
