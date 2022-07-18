# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# get a list of the country names to use for iterating through the text (hardcoding:/)
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

# get html code from website
url = 'https://futurefreespeech.com/global-handbook-on-hate-speech-laws/#post-1391-_Toc56591732'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# remove hyperlinks to facilitate finding the headers later
for x in soup.find_all('a'):
  x.replaceWithChildren()
  
# make list to store tuples (country, legislation)
laws=[]
# iterate through the text with the help of headers and country list
for text in countries: 
  target = soup.find('h1',text=text)
  # keep the text under the header
  for sib in target.find_next_siblings():
      if sib.name=="h1":
          break
      else:
          # store in list
          laws.append(tuple((text, sib.text)))
          
# create dataframe using the tuple list
df = pd.DataFrame.from_records(laws, columns =['Country', 'Legislation'])
# make index column a regurlar column
df.reset_index(inplace=True)

# create multindex
df.set_index([ "Country", "index",], inplace=True)
df.sort_index(inplace=True)
# write to csv
df.to_csv('hate_laws.zip', index=False)
