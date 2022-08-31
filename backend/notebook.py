from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import pandas as pd
import pickle

from utils import load, save

# df = pd.read_csv('small_temp_movie_corpus.csv', names=['title', 'genre', 'year', 'summary']) # can make this an sql query

# model = SentenceTransformer('all-MiniLM-L6-v2')

# encodings = model.encode(df['summary']) # can call encoding directly or...

# df['encodings'] = [np.array(x) for x in encodings]

# save (df, "data_frame.pkl")

# # save encodings and load in previous model from disk later
# save (encodings, "encodings.pkl")

# # don't know if we really need this
# save (model, "model.pkl")
# print ("model saved!")

# load in model/encodings from disk
# print('loading encodings')
# encodings = load ("encodings.pkl")

df = load("data_frame.pkl")

print (df['encodings'])

# print (df)

# for x in encodings:
#     print (x.shape)

# print('loading model')
model = load ("model.pkl")

# K = 10
my_sentence = 'time travel'

# print('evaluating movies')
# # evaluate cosine similarity from sentence encoding to all summary encodings
similarities_df = pd.DataFrame(cosine_similarity(model.encode (my_sentence).reshape(1, -1), df['encodings'].to_list())[0], columns=['values'])

# # copy over title
similarities_df['title'] = df['title']

# # first 5 films with their similarlity
print (similarities_df.head())
# print(similarities_df.nlargest (K, columns=['values']))
