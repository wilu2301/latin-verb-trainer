from bs4 import BeautifulSoup
import requests
from backend.db.verb import add_verb

from backend.utils import set_nested


class LayoutError(Exception):
    pass


def get_html(word: str) -> str:
    """
    Gets the html of the Frag Caesar Page
    :param word: The Verb
    :return:
    """
    url = f"https://www.frag-caesar.de/lateinwoerterbuch/{word}-uebersetzung.html"

    return requests.get(url).text


def parse_verb(html: str) -> list[list]:
    """
    Parses the HTML to a list
    :param html: HTML
    :return: JSON obj
    """

    forms = []

    search = BeautifulSoup(html, "html.parser")
    tables = search.find_all("div", {"class": "toggle"})
    for t in range(10):
        table_parts = tables[t].find_all("td", {"class": "eh"})

        person = []
        for p in range(0, 24, 2):

            # Check if a verb has multiple forms
            if len(table_parts[p].find_all("br")) >= 2:
                words = str(table_parts[p]).split("<br/>")

                # Removes the Last BR
                words.pop()

                word_part = []
                for w in words:
                    part = BeautifulSoup(w, "html.parser").get_text()

                    if part == "existiert nicht":
                        part = None

                    word_part.append(part)

                word = word_part

            else:
                word = table_parts[p].get_text()
                if word == "existiert nicht":
                    word = None

            person.append(word)

        forms.append(person)

    return forms


def transform_verb_to_json(forms: list) -> dict:
    """
    Transform to a dict and replace non-existent with None
    :param forms: forms in a list
    :return: json obj
    """

    """
    Document Structure
    {
    'preset: {
        'active': {
            'indicative': [...]
            'conjunctive': [...]
        }
        'passive':{
            ...
        }
    }  
    """

    document = {

    }

    # present
    set_nested(document, ["praesens", "active", "indicative"], forms[0][:6])
    set_nested(document, ["praesens", "passive", "indicative"], forms[0][6:12])
    # Konj
    set_nested(document, ["praesens", "active", "conjunctive"], forms[1][:6])
    set_nested(document, ["praesens", "passive", "conjunctive"], forms[1][6:12])

    # Imp
    set_nested(document, ["imperfekt", "active", "indicative"], forms[2][:6])
    set_nested(document, ["imperfekt", "passive", "indicative"], forms[2][6:12])
    # Konj
    set_nested(document, ["imperfekt", "active", "conjunctive"], forms[3][:6])
    set_nested(document, ["imperfekt", "passive", "conjunctive"], forms[3][6:12])

    # Futur I
    set_nested(document, ["futur1", "active", "indicative"], forms[4][:6])
    set_nested(document, ["futur1", "passive", "indicative"], forms[4][6:12])

    # Perfect
    set_nested(document, ["perfekt", "active", "indicative"], forms[5][:6])
    set_nested(document, ["perfekt", "passive", "indicative"], forms[5][6:12])
    # Konj
    set_nested(document, ["perfekt", "active", "conjunctive"], forms[6][:6])
    set_nested(document, ["perfekt", "passive", "conjunctive"], forms[6][6:12])

    # Plusquamperfekt
    set_nested(document, ["plusquamperfekt", "active", "indicative"], forms[7][:6])
    set_nested(document, ["plusquamperfekt", "passive", "indicative"], forms[7][6:12])
    # Konj
    set_nested(document, ["plusquamperfekt", "active", "conjunctive"], forms[8][:6])
    set_nested(document, ["plusquamperfekt", "passive", "conjunctive"], forms[8][6:12])

    # Futur2
    set_nested(document, ["futur2", "active", "indicative"], forms[9][:6])
    set_nested(document, ["futur2", "passive", "indicative"], forms[9][6:12])

    return document


def rip_verb_by_name(word: str) -> None:
    """
    Extracts the entire Verb list from Frag Caesar
    :param word: 
    :return:
    """

    html = get_html(word)
    try:
        parsed = parse_verb(html)
    except IndexError:
        raise LayoutError
    transformed = transform_verb_to_json(parsed)
    add_verb(transformed)


# noinspection PyShadowingNames
def rip_verb_by_url(url: str) -> None:
    """
    Extracts the entire Verb list from Frag Caesar
    :param url:
    :return:
    """

    html = requests.get(url).text
    parsed = parse_verb(html)
    transformed = transform_verb_to_json(parsed)
    add_verb(transformed)


if __name__ == "__main__":
    verb = input("Verb:")
    try:
        rip_verb_by_name(verb)
    except LayoutError:
        url = input("URL:")
        rip_verb_by_url(url)
