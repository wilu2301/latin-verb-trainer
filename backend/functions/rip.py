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
    address = f"https://www.frag-caesar.de/lateinwoerterbuch/{word}-uebersetzung.html"

    return requests.get(address).text


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


def transform_verb_forms_to_json(forms: list) -> dict:
    """
    Transform verb_forms to a dict
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


def transform_verb_to_json(forms: dict, information: dict):
    document = {}

    document.update(forms)
    document.update(information)

    return document


def parse_verb_information(html: str) -> dict:
    """
    Parses Konjunktion, Infinitive, PPP and german translation
    :param html: html
    :return: formatted as dict
    """

    search = BeautifulSoup(html, "html.parser")
    table = search.find_all("div", {"class": "table-responsive"})[0]

    # get konjugation
    konjugation = table.find_all("td", {"class": "eh"})[1].get_text()

    # get translations
    translation_field = table.find_all("td", {"class": "eh"})[3]
    translations_split = str(translation_field).split("<br/>")

    # Removes the Last BR
    translations_split.pop()

    translations = []
    for t in translations_split:
        part = BeautifulSoup(t, "html.parser").get_text()
        translations.append(part)

    # get infinitive
    infinitive = table.find_all("td", {"class": "eh2"})[0].get_text()

    # Get PPP
    ppp = search.find_all("table")[29].find_all("td", {"class": "eh"})[0].get_text()

    return {"translations": translations, "konjugation": konjugation, "infinitive": infinitive, "ppp": ppp}


def rip_verb_by_name(word: str) -> None:
    """
    Extracts the entire Verb list from Frag Caesar
    :param word: 
    :return:
    """

    html = get_html(word)
    try:
        parsed_forms = parse_verb(html)
        parsed_information = parse_verb_information(html)
    except IndexError:
        raise LayoutError

    transform_forms = transform_verb_forms_to_json(parsed_forms)
    transformed = transform_verb_to_json(transform_forms, parsed_information)

    add_verb(transformed)


# noinspection PyShadowingNames
def rip_verb_by_url(url: str) -> None:
    """
    Extracts the entire Verb list from Frag Caesar
    :param url:
    :return:
    """

    html = requests.get(url).text

    parsed_forms = parse_verb(html)
    parsed_information = parse_verb_information(html)

    transform_forms = transform_verb_forms_to_json(parsed_forms)
    transformed = transform_verb_to_json(transform_forms, parsed_information)

    add_verb(transformed)


if __name__ == "__main__":
    verb = input("Verb:")
    try:
        rip_verb_by_name(verb)
    except LayoutError:
        url = input("URL:")
        rip_verb_by_url(url)
