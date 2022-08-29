# original code can be found here: https://towardsdatascience.com/semantic-similarity-using-transformers-8f3cb5bf66d6
# using a powerful model (e.g. transformer) to encode sentences to get their embeddings and then use a similarity metric (e.g. cosine similarity).

# imports
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# load and read dataset of hate_laws
df = pd.read_csv("hate_laws.csv")
