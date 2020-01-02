import pandas as pd 
from app import routes

def run():
    data = pd.read_csv('./analysis/' + routes.FILENAME)
    return data.columns