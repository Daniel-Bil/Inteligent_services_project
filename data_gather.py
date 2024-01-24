import wikipediaapi
import requests
import json
import os
wiki_wiki = wikipediaapi.Wikipedia('IntelligentServicesProject (dxxx409@gmail.com)', 'en')
def wikipedia(title):


    page_py = wiki_wiki.page(title)
    print(page_py)
    print("Page - Title: %s" % page_py.title)
    print("Page - Exists: %s" % page_py.exists())
    print("Page - Categories: %s" % page_py.categories)
    sections = [s.title for s in page_py.sections]
    print("Page - Sections: %s" % sections)

    d_p = {"Title": page_py.title,
           "Summary": page_py.summary,
           "Text": page_py.text,
           "Sections": sections,
           "Categories": list(page_py.categories)}
    return dict(d_p)


def get_random_wikipedia_pages(limit=5):
    """
    Fetches a list of random Wikipedia page titles.
    """
    # Wikipedia API endpoint
    endpoint = "https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": limit
    }

    # Making the request to the Wikipedia API
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Extracting the random page titles
    random_pages = data["query"]["random"]
    return random_pages

def save_article():
    pass

if __name__ == '__main__':
    save_path = f'./pages'
    number_of_pages=10
    article_title = "Python (programming language)"
    wikipedia(article_title)
    titles = []
    for i in range(number_of_pages):

        random_pages = get_random_wikipedia_pages(limit=5)
        for page in random_pages:
            print(page["title"])

            d_p = wikipedia(page["title"])
            file_path = f"{save_path}/{d_p['Title']}"
            if not os.path.exists(file_path):
                try:
                    with open(file_path, 'w') as fp:
                        json.dump(d_p, fp, indent=4)
                except:
                    print("Error")

