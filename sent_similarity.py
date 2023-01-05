import pandas as pd
import numpy as np
import nltk; nltk.download('punkt')
import itertools


from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
from itertools import product
from ast import literal_eval
from zipfile import *
 
 
df = pd.read_csv("hate_laws.csv")

# which countries do not have laws on hate speech
nolaw = df['Country'].loc[df['Legislation'].str.startswith('–')].to_list()

# leave countries that contain legislation for hate speech
df = df[df['Legislation'].str.startswith('–')== False]
 

file_name = "/home/akorre/country_laws.zip/"
  
# opening the zip file in READ mode
with ZipFile(file_name, 'r') as zip:
    # printing all the contents of the zip file
    zip.printdir()
    # extracting all the files
    zip.extractall()
    
    
# read all country csvs
# giving file extension
ext = ('.csv')
 
# iterating over all files
for files in os.listdir("/home/akorre/hate_laws/"):
    if files.endswith(ext):
        s = pd.read_csv(files)

# drop nan values
s = s.dropna()

# get list of countries
countries = df['Country'].to_list()
countries = [x for x in countries if x not in nolaw]

# country coupling
cpairs = list(itertools.combinations(countries, 2))

def roberta_similarity_sent(x, y):
  # empty list to store the scores
  scores = [] 

  # read country csv pair
  c1 = pd.read_csv("%s.csv" %x)
  c2 = pd.read_csv("%s.csv" %y)
  
  # this must be done beforehand
  c1 = c1.dropna()
  c2 = c2.dropna()

  # put the sentences into lists
  c1list = c1['Legislation'].to_list()
  c2list = c2['Legislation'].to_list()

  # pair the sentences for each country
  sentlist = list(itertools.product(c1list, c2list))

  # call model
  model = SentenceTransformer('stsb-roberta-large')

  
  for item in sentlist:
    # encode sentences to get their embeddings
    embedding1 = model.encode(item[0], convert_to_tensor=True)
    embedding2 = model.encode(item[1], convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    scores.append((item, cosine_scores.item()))
  return scores

  
result = []
for item in cpairs:
  result.append((item,roberta_similarity_sent(item[0], item[1])))


with open("/home/akorre/result/hate_results.txt", "w") as f:
  for item in result:
    f.write(str(item))
  f.close()
