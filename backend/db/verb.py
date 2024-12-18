from backend.db.engine import db


def add_verb(content: dict) -> None:
    """
    Adds a Verb to the Database
    :param content: the Data JSON formatted
    :return
    """

    db["verbs"].insert_one(content)
