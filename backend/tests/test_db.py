from backend.db import verb
import pytest

pytest_plugins = ('pytest_asyncio')


@pytest.mark.asyncio
async def test_get_random_infinitive():
    """
    Tests if the db returns a random Infinitive
    :return:
    """

    res = verb.get_random_infinitive()
    assert True
