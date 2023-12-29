import requests
from bs4 import BeautifulSoup
import os
from slugify import slugify

def scrape_wikipedia_page(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the lang attribute in the html tag
        lang = soup.html.get('lang')

        # Find the main content by selecting the appropriate HTML elements
        main_content = soup.find('div', {'id': 'mw-content-text'})

        # Extract text from the main content
        main_text = main_content.get_text()

        return lang, main_text
    else:
        print(f"Failed to retrieve the page {url}. Status code:", response.status_code)
        return None, None

def save_text_to_file(language, text):
    # Create a directory to store text files if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Create a valid filename using the slugify library for languages that are weird
    filename = f"output/{slugify(language)}_hate_speech.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def scrape_wikipedia_pages(urls):
    for url in urls:
        # Scrape the Wikipedia page
        lang, text = scrape_wikipedia_page(url)

        if lang and text:
            # Save the text to a txt file
            save_text_to_file(lang, text)

if __name__ == "__main__":    
    wiki_urls = [
        "https://en.wikipedia.org/wiki/Hate_speech",
        "https://ja.wikipedia.org/wiki/%E3%83%98%E3%82%A4%E3%83%88%E3%82%B9%E3%83%94%E3%83%BC%E3%83%81",
        "https://el.wikipedia.org/wiki/%CE%A1%CE%B7%CF%84%CE%BF%CF%81%CE%B9%CE%BA%CE%AE_%CE%BC%CE%AF%CF%83%CE%BF%CF%85%CF%82",
        "https://bg.wikipedia.org/wiki/%D0%95%D0%B7%D0%B8%D0%BA_%D0%BD%D0%B0_%D0%BE%D0%BC%D1%80%D0%B0%D0%B7%D0%B0%D1%82%D0%B0",
        "https://mk.wikipedia.org/wiki/%D0%93%D0%BE%D0%B2%D0%BE%D1%80_%D0%BD%D0%B0_%D0%BE%D0%BC%D1%80%D0%B0%D0%B7%D0%B0",
        "https://de.wikipedia.org/wiki/Hassrede",
        "https://fr.wikipedia.org/wiki/Discours_de_haine",
        "https://sq.wikipedia.org/wiki/Gjuha_e_urrejtjes",
        "https://tr.wikipedia.org/wiki/Nefret_s%C3%B6ylemi",
        "https://es.wikipedia.org/wiki/Discurso_de_odio",
        "https://pt.wikipedia.org/wiki/Discurso_de_%C3%B3dio",
        "https://zh.wikipedia.org/wiki/%E4%BB%87%E6%81%A8%E8%A8%80%E8%AB%96",
        "https://ht.wikipedia.org/wiki/Diskou_rayisab",
        "https://nl.wikipedia.org/wiki/Haatzaaien",
        "https://ru.wikipedia.org/wiki/%D0%AF%D0%B7%D1%8B%D0%BA_%D0%B2%D1%80%D0%B0%D0%B6%D0%B4%D1%8B",
        "https://sr.wikipedia.org/wiki/%D0%93%D0%BE%D0%B2%D0%BE%D1%80_%D0%BC%D1%80%D0%B6%D1%9A%D0%B5",
        "https://uk.wikipedia.org/wiki/%D0%9C%D0%BE%D0%B2%D0%B0_%D0%B2%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D0%B5%D1%87%D1%96",
        "https://bs.wikipedia.org/wiki/Govor_mr%C5%BEnje",
        "https://ca.wikipedia.org/wiki/Discurs_d%27odi",
        "https://et.wikipedia.org/wiki/Vaenuk%C3%B5ne",
        "https://eu.wikipedia.org/wiki/Gorroto-diskurtso",
        "https://hr.wikipedia.org/wiki/Govor_mr%C5%BEnje",
        "https://it.wikipedia.org/wiki/Incitamento_all%27odio",
        "https://hu.wikipedia.org/wiki/Gy%C5%B1l%C3%B6letbesz%C3%A9d",
        "https://no.wikipedia.org/wiki/Hatprat",
        "https://pl.wikipedia.org/wiki/Mowa_nienawi%C5%9Bci",
        "https://ro.wikipedia.org/wiki/Discurs_de_instigare_la_ur%C4%83",
        "https://sk.wikipedia.org/wiki/Nen%C3%A1vistn%C3%BD_prejav",
        "https://sl.wikipedia.org/wiki/Sovra%C5%BEni_govor",
        "https://sh.wikipedia.org/wiki/Govor_mr%C5%BEnje",
        "https://fi.wikipedia.org/wiki/Vihapuhe",
        "https://sv.wikipedia.org/wiki/Hatpropaganda",
        "https://is.wikipedia.org/wiki/Hatursor%C3%B0r%C3%A6%C3%B0a",
        "https://cs.wikipedia.org/wiki/Hate_speech",
        "https://hy.wikipedia.org/wiki/%D4%B1%D5%BF%D5%A5%D5%AC%D5%B8%D6%82%D5%A9%D5%B5%D5%A1%D5%B6_%D5%AD%D5%B8%D5%BD%D6%84",
        "https://ur.wikipedia.org/wiki/%D9%86%D9%81%D8%B1%D8%AA_%D8%A7%D9%86%DA%AF%DB%8C%D8%B2_%DA%A9%D9%84%D8%A7%D9%85",
        "https://ar.wikipedia.org/wiki/%D8%AE%D8%B7%D8%A7%D8%A8_%D8%A7%D9%84%D9%83%D8%B1%D8%A7%D9%87%D9%8A%D8%A9",
        "https://fa.wikipedia.org/wiki/%D9%86%D9%81%D8%B1%D8%AA%E2%80%8C%D9%BE%D8%B1%D8%A7%DA%A9%D9%86%DB%8C",
        "https://pnb.wikipedia.org/wiki/%D9%86%D9%81%D8%B1%D8%AA_%D8%A7%D9%86%DA%AF%DB%8C%D8%B2_%DA%A9%D9%84%D8%A7%D9%85",
        "https://ckb.wikipedia.org/wiki/%DA%AF%D9%88%D9%88%D9%81%D8%AA%D8%A7%D8%B1%DB%8C_%DA%A9%DB%8C%D9%86%DB%95%DB%8C%DB%8C",
        "https://he.wikipedia.org/wiki/%D7%94%D7%A1%D7%AA%D7%94",
        "https://af.wikipedia.org/wiki/Haatspraak",
        "https://ko.wikipedia.org/wiki/%EC%A6%9D%EC%98%A4%EC%96%B8%EC%84%A4",
        "https://id.wikipedia.org/wiki/Ujaran_kebencian",
        "https://uz.wikipedia.org/wiki/Nafrat_tili",
        "https://vi.wikipedia.org/wiki/Ph%C3%A1t_ng%C3%B4n_th%C3%B9_h%E1%BA%ADn",
        "https://bh.wikipedia.org/wiki/%E0%A4%B9%E0%A5%87%E0%A4%9F_%E0%A4%B8%E0%A5%8D%E0%A4%AA%E0%A5%80%E0%A4%9A",
        "https://hi.wikipedia.org/wiki/%E0%A4%A6%E0%A5%8D%E0%A4%B5%E0%A5%87%E0%A4%B7%E0%A4%AA%E0%A5%82%E0%A4%B0%E0%A5%8D%E0%A4%A3_%E0%A4%AD%E0%A4%BE%E0%A4%B7%E0%A4%A3",
        "https://th.wikipedia.org/wiki/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%97%E0%B8%B8%E0%B8%A9%E0%B8%A7%E0%B8%B2%E0%B8%88%E0%B8%B2",
        "https://my.wikipedia.org/wiki/%E1%80%A1%E1%80%99%E1%80%AF%E1%80%94%E1%80%BA%E1%80%B8%E1%80%85%E1%80%80%E1%80%AC%E1%80%B8%E1%80%95%E1%80%BC%E1%80%B1%E1%80%AC%E1%80%81%E1%80%BC%E1%80%84%E1%80%BA%E1%80%B8"

    ]

    
    scrape_wikipedia_pages(wiki_urls)
