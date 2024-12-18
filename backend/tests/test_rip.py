from backend.functions import rip

MOCK_DATA_VERB = [['ulcisco', 'ulciscis', 'ulciscit', 'ulciscimus', 'ulciscitis', 'ulciscunt', 'ulciscor',
                   ['ulcisceris', 'ulciscere'], 'ulciscitur', 'ulciscimur', 'ulciscimini', 'ulciscuntur'],
                  ['ulciscam', 'ulciscas', 'ulciscat', 'ulciscamus', 'ulciscatis', 'ulciscant', 'ulciscar',
                   ['ulciscaris', 'ulciscare'], 'ulciscatur', 'ulciscamur', 'ulciscamini', 'ulciscantur'],
                  ['ulciscebam', 'ulciscebas', 'ulciscebat', 'ulciscebamus', 'ulciscebatis', 'ulciscebant',
                   'ulciscebar',
                   ['ulciscebaris', 'ulciscebare'], 'ulciscebatur', 'ulciscebamur', 'ulciscebamini', 'ulciscebantur'],
                  ['ulciscerem', 'ulcisceres', 'ulcisceret', 'ulcisceremus', 'ulcisceretis', 'ulciscerent',
                   'ulciscerer',
                   ['ulciscereris', 'ulciscerere'], 'ulcisceretur', 'ulcisceremur', 'ulcisceremini', 'ulciscerentur'],
                  ['ulciscam', 'ulcisces', 'ulciscet', 'ulciscemus', 'ulciscetis', 'ulciscent', 'ulciscar',
                   ['ulcisceris', 'ulciscere'], 'ulciscetur', 'ulciscemur', 'ulciscemini', 'ulciscentur'],
                  [None, None, None, None, None, None, 'ultus sum', 'ultus es', 'ultus est', 'ulti sumus', 'ulti estis',
                   'ulti sunt'],
                  [None, None, None, None, None, None, 'ultus sim', 'ultus sis', 'ultus sit', 'ulti simus',
                   'ulti sitis',
                   'ulti sint'],
                  [None, None, None, None, None, None, 'ultus eram', 'ultus eras', 'ultus erat', 'ulti eramus',
                   'ulti eratis', 'ulti erant'],
                  [None, None, None, None, None, None, 'ultus essem', 'ultus esses', 'ultus esset', 'ulti essemus',
                   'ulti essetis', 'ulti essent'],
                  [None, None, None, None, None, None, 'ultus ero', 'ultus eris', 'ultus erit', 'ulti erimus',
                   'ulti eritis', 'ulti erunt']]


def test_http():
    """
    Test the response of Frag Caesar
    :return:
    """
    assert rip.get_html("ulcisci") is not None


def test_verb_extractor():
    """
    Tests the Verb to JSON Converter
    :return:
    """

    VERB = "ulcisci"
    EXPECTED = MOCK_DATA_VERB

    result = rip.parse_verb(rip.get_html(VERB))

    assert EXPECTED == result


def test_verb_transform():
    DATA = MOCK_DATA_VERB

    EXPECTED = {'praesens': {
        'active': {'indicative': ['ulcisco', 'ulciscis', 'ulciscit', 'ulciscimus', 'ulciscitis', 'ulciscunt'],
                   'conjunctive': ['ulciscam', 'ulciscas', 'ulciscat', 'ulciscamus', 'ulciscatis', 'ulciscant']},
        'passive': {'indicative': ['ulciscor', ['ulcisceris', 'ulciscere'], 'ulciscitur', 'ulciscimur', 'ulciscimini',
                                   'ulciscuntur'],
                    'conjunctive': ['ulciscar', ['ulciscaris', 'ulciscare'], 'ulciscatur', 'ulciscamur', 'ulciscamini',
                                    'ulciscantur']}}, 'imperfekt': {'active': {
        'indicative': ['ulciscebam', 'ulciscebas', 'ulciscebat', 'ulciscebamus', 'ulciscebatis', 'ulciscebant'],
        'conjunctive': ['ulciscerem', 'ulcisceres', 'ulcisceret', 'ulcisceremus', 'ulcisceretis', 'ulciscerent']},
        'passive': {'indicative': ['ulciscebar',
                                   ['ulciscebaris',
                                    'ulciscebare'],
                                   'ulciscebatur',
                                   'ulciscebamur',
                                   'ulciscebamini',
                                   'ulciscebantur'],
                    'conjunctive': ['ulciscerer',
                                    ['ulciscereris',
                                     'ulciscerere'],
                                    'ulcisceretur',
                                    'ulcisceremur',
                                    'ulcisceremini',
                                    'ulciscerentur']}},
        'futur1': {'active': {
            'indicative': ['ulciscam', 'ulcisces', 'ulciscet', 'ulciscemus', 'ulciscetis', 'ulciscent']},
            'passive': {
                'indicative': ['ulciscar', ['ulcisceris', 'ulciscere'], 'ulciscetur', 'ulciscemur',
                               'ulciscemini', 'ulciscentur']}}, 'perfekt': {
            'active': {'indicative': [None, None, None, None, None, None],
                       'conjunctive': [None, None, None, None, None, None]},
            'passive': {'indicative': ['ultus sum', 'ultus es', 'ultus est', 'ulti sumus', 'ulti estis', 'ulti sunt'],
                        'conjunctive': ['ultus sim', 'ultus sis', 'ultus sit', 'ulti simus', 'ulti sitis',
                                        'ulti sint']}}, 'plusquamperfekt': {
            'active': {'indicative': [None, None, None, None, None, None],
                       'conjunctive': [None, None, None, None, None, None]}, 'passive': {
                'indicative': ['ultus eram', 'ultus eras', 'ultus erat', 'ulti eramus', 'ulti eratis', 'ulti erant'],
                'conjunctive': ['ultus essem', 'ultus esses', 'ultus esset', 'ulti essemus', 'ulti essetis',
                                'ulti essent']}},
        'futur2': {'active': {'indicative': [None, None, None, None, None, None]}, 'passive': {
            'indicative': ['ultus ero', 'ultus eris', 'ultus erit', 'ulti erimus', 'ulti eritis',
                           'ulti erunt']}}}

    result = rip.transform_verb_to_json(DATA)

    assert result == EXPECTED
