import random

from ..db.engine import db


def add_verb(content: dict) -> None:
    """
    Adds a Verb to the Database
    :param content: the Data JSON formatted
    :return
    """

    db["verbs"].insert_one(content)


def get_verb(verb: str) -> dict:
    """
    Gets the Verb from the db
    :param verb:
    :return:
    """

    result = db["verbs"].find_one({"infinitive": verb})
    if result:
        result.pop("_id",None)
        return result

    else:
        return {}


def get_random_infinitive() -> str:
    """
    Returns a random infinitive
    :return:
    """
    pipeline = [
        {"$sample": {"size": 1}}
    ]

    return list(db["verbs"].aggregate(pipeline))[0]["infinitive"]
