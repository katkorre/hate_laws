# original code can be found here: https://towardsdatascience.com/semantic-similarity-using-transformers-8f3cb5bf66d6
# using a powerful model (e.g. transformer) to encode sentences to get their embeddings and then use a similarity metric (e.g. cosine similarity).

# imports
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# load and read dataset of hate_laws
df = pd.read_csv("/home/akorre/hate_laws/hate_laws.csv")

# we use roberta for the task of semantic similarity
model = SentenceTransformer('stsb-roberta-large')

# we need to have pairs of all possible language combinations
from itertools import combinations
es = list(combinations(sample['Country'], 2))

# function that takes as input a dataframe. 
def scores(data): 
  scores = []
  # for loop that iterates the elements of the list of pairs.
  for item in es: 
    x = data.loc[data['Country'] == item[0], 'Legislation'].to_list()
    y = data.loc[data['Country'] == item[1], 'Legislation'].to_list()
    # encode sentences to get their embeddings
    embedding1 = model.encode(x, convert_to_tensor=True)
    embedding2 = model.encode(y, convert_to_tensor=True)
    # calculate cosine similarity between the pairs. 
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    scores.append((f"{item}:", cosine_scores.item()))
  return scores
