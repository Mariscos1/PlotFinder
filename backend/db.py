import pandas as pd
import numpy as np

from utils import load
# MOCK DB

def select_movies (min_year=0, max_year=999999999):

    # these lines would be replaced by an SQL query
    df = load ("df_encodings.pkl")
    df = df[(min_year <= df['year']) * (df['year'] <= max_year)]
    return df