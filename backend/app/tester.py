import pandas as pd 
from app import routes
import os

def run():
    try:
        data = pd.read_csv('./app/' + routes.FILENAME)
        return data.head(50)
    except:
        return 'The file does not yet exist! Please upload one.'
