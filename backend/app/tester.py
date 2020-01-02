import pandas as pd 
from app import routes
import os

def run():
    try:
        data = pd.read_csv('./app/analysis/' + routes.FILENAME)
        os.remove('./app/analysis/' + routes.FILENAME)
        return data
    except:
        return 'The file does not yet exist! Please upload one.'
