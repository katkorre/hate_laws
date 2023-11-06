import pandas as pd
import re

# read scraped unprocessed file
df = pd.read_csv("hate_laws.csv")

law_column = 'Legislation'

# we want to remove the sentences that start with the following string. 
pattern_to_remove = "Status of country in relation to the ICCPR"

# remove it with this function
def remove_unwanted_text(text):
    index = text.find(pattern_to_remove)
    if index != -1:
        return text[:index]
    return text

df[law_column] = df[law_column].apply(remove_unwanted_text)

# filter out rows that contain only hyphens or hyphens with newline characters 
df = df[~df[law_column].str.replace('\n', '').str.strip().eq('–')]

# save new file
df.to_csv("hate_laws_processed.csv", index=False)
