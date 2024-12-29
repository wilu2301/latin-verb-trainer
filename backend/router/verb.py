from fastapi import APIRouter
from backend.db import verb as db

router = APIRouter(
    prefix="/verb"
)

@router.get("")
async def get_verb(infinitive: str) -> dict:
    """
    Gets the complete verb data
    :param infinitive: the query
    :return:
    """

    return db.get_verb(infinitive)

@router.get("/random_infinitive")
async def get_random_infinitive() -> str:
    """
    Returns a random Verb of the Database
    :return: Random Verb
    """

    return db.get_random_infinitive()

