import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import os
import itertools
nltk.download('punkt')

from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
from itertools import product
from ast import literal_eval
from pylab import savefig
from zipfile import ZipFile
 
# get a list of the country names to use for iterating through the text
countries = ["AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ANTIGUA AND BARBUDA","ARGENTINA", "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN",
             "BAHAMAS", "BAHRAIN", "BANGLADESH", "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN", "BHUTAN", "BOLIVIA", "BOSNIA AND HERZEGOVINA", "BOTSWANA",
             "BRAZIL", "BRUNEI DARUSSALAM", "BULGARIA", "BURKINA FASO", "BURUNDI", "CABO VERDE", "CAMBODIA", "CAMEROON", "CANADA", "CENTRAL AFRICAN REPUBLIC", "CHAD",
             "CHILE", "CHINA", "COLOMBIA", "COMOROS", "CONGO BRAZZAVILLE", "COSTA RICA", "COTE D’IVOIRE", "CROATIA", "CUBA", "CYPRUS", "CZECH REPUBLIC", "DEMOCRATIC PEOPLE’S REPUBLIC OF KOREA",
             "DEMOCRATIC REPUBLIC OF THE CONGO", "DENMARK", "DJIBOUTI", "DOMINICA", "DOMINICAN REPUBLIC", "ECUADOR", "EGYPT", "EL SALVADOR", "EQUATORIAL GUINEA",
             "ERITREA", "ESTONIA", "ESWATINI", "ETHIOPIA", "FIJI", "FINLAND", "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA", "GREECE", "GRENADA",
             "GUATEMALA", "GUINEA", "GUINEA BISSAU", "GUYANA", "HAITI", "HONDURAS", "HUNGARY", "ICELAND", "INDIA", "INDONESIA", "IRAN (Islamic Republic of)", "IRAQ", 
             "IRELAND", "ISRAEL", "ITALY" , "JAMAICA", "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KUWAIT", "KYRGYZSTAN", "LATVIA", "LEBANON", "LESOTHO",
             "LIBERIA", "LIBYA", "LAO PEOPLE’S DEMOCRATIC REPUBLIC", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG", "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES",
             "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR", "NAMIBIA", "NAURU", "NEPAL", "THE NETHERLANDS", "NEW ZEALAND", "NICARAGUA", "NIGER", "NIGERIA", 
             "NORTH MACEDONIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PANAMA", "PAPUA NEW GUINEA", "PARAGUAY", "PERU", "THE PHILIPPINES", "POLAND", "PORTUGAL",
             "QATAR", "REPUBLIC OF KOREA", "ROMANIA", "RUSSIAN FEDERATION", "RWANDA", "SAINT KITTS AND NEVIS", "SAINT LUCIA", "SAINT VINCENT AND THE GRENADINES", 
             "STATE OF PALESTINE", "SAMOA", "SAN MARINO", "SAO TOME AND PRINCIPE", "SAUDI ARABIA", "SENEGAL", "SERBIA", "SEYCHELLES", "SIERRA LEONE", "SINGAPORE",
             "SLOVAKIA", "SLOVENIA", "SOLOMON ISLANDS", "SOMALIA", "SOUTH AFRICA", "SOUTH SUDAN", "SPAIN", "SRI LANKA", "SURINAME", "SWEDEN", "SWITZERLAND",
             "SYRIAN ARAB REPUBLIC", "TAJIKISTAN", "TANZANIA", "THAILAND", "TIMOR-LESTE", "TOGO", "TONGA", "TRINIDAD AND TOBAGO", "TUNISIA", "TURKEY",
             "TURKMENISTAN", "TUVALU", "UGANDA", "UKRAINE", "UNITED ARAB EMIRATES", "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND", "UNITED STATES OF AMERICA",
             "URUGUAY", "UZBEKISTAN", "VANUATU", "VENEZEULA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE"]
# specifying the zip file name
file_name = "country_laws.zip"
  
# opening the zip file in READ mode
with ZipFile(file_name, 'r') as zip:
    # printing all the contents of the zip file
    zip.printdir()
    # extracting all the files
    print('Extracting all the files now...')
    zip.extractall()
    print('Done!')
    
# read all country csvs
# giving file extension
ext = ('.csv')
 
# iterating over all files
for files in os.listdir("/content/"):
    if files.endswith(ext):
        s = pd.read_csv(files)

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

print(result)
