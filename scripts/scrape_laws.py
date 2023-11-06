import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the webpage content
url = "https://futurefreespeech.com/global-handbook-on-hate-speech-laws/#post-1391-_Toc56591825"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the section containing country names
country_section = soup.find("h2", text="National Level").find_next("table")

# Extract country names from the two ordered lists
countries = []
for ol in country_section.find_all("ol"):
    country_links = ol.find_all("a")
    for link in country_links:
        countries.append(link.text)

# Remove hyperlinks to facilitate finding the headers later
for x in soup.find_all('a'):
  x.replaceWithChildren()

# Make list to store tuples (country, legislation)
laws=[]
# Iterate through the text with the help of headers and country list
for text in countries: 
  target = soup.find('h1',text=text)
  # Keep the text under the header
  for sib in target.find_next_siblings():
      if sib.name=="h1":
          break
      else:
          # Store in list
          laws.append(tuple((text, sib.text)))

# Create dataframe using the tuple list
df = pd.DataFrame.from_records(laws, columns =['Country', 'Legislation'])

# Make index column a regular column
df.reset_index(inplace=True)

# Join everything
df = df.groupby(['Country'])['Legislation'].apply(' '.join).reset_index()

# Write to csv
df.to_csv('hate_laws.zip', index=False)
