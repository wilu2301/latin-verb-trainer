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


def test_verb_get_information():
    """
    Tests the gathering of translation and Konjugation
    :return:
    """

    EXPECTED = {'translations': ['rächen', 'sich rächen', 'sich rächen (an/für)', 'strafen'],
                'konjugation': 'konsonantische Konjugation', 'infinitive': 'ulcisci', 'ppp': 'ultus'}

    result = rip.parse_verb_information(rip.get_html("ulcisci"))

    assert result == EXPECTED


def test_verb_transform():
    DATA_FORMS = MOCK_DATA_VERB
    DATA_INFORMATION = {'translations': ['rächen', 'sich rächen', 'sich rächen (an/für)', 'strafen'],
                        'konjugation': 'konsonantische Konjugation', 'infinitive': 'ulcisci', 'ppp': 'ultus'}

    EXPECTED = {'futur1': {'active': {'indicative': ['ulciscam',
                                                     'ulcisces',
                                                     'ulciscet',
                                                     'ulciscemus',
                                                     'ulciscetis',
                                                     'ulciscent']},
                           'passive': {'indicative': ['ulciscar',
                                                      ['ulcisceris', 'ulciscere'],
                                                      'ulciscetur',
                                                      'ulciscemur',
                                                      'ulciscemini',
                                                      'ulciscentur']}},
                'futur2': {'active': {'indicative': [None, None, None, None, None, None]},
                           'passive': {'indicative': ['ultus ero',
                                                      'ultus eris',
                                                      'ultus erit',
                                                      'ulti erimus',
                                                      'ulti eritis',
                                                      'ulti erunt']}},
                'imperfekt': {'active': {'conjunctive': ['ulciscerem',
                                                         'ulcisceres',
                                                         'ulcisceret',
                                                         'ulcisceremus',
                                                         'ulcisceretis',
                                                         'ulciscerent'],
                                         'indicative': ['ulciscebam',
                                                        'ulciscebas',
                                                        'ulciscebat',
                                                        'ulciscebamus',
                                                        'ulciscebatis',
                                                        'ulciscebant']},
                              'passive': {'conjunctive': ['ulciscerer',
                                                          ['ulciscereris', 'ulciscerere'],
                                                          'ulcisceretur',
                                                          'ulcisceremur',
                                                          'ulcisceremini',
                                                          'ulciscerentur'],
                                          'indicative': ['ulciscebar',
                                                         ['ulciscebaris', 'ulciscebare'],
                                                         'ulciscebatur',
                                                         'ulciscebamur',
                                                         'ulciscebamini',
                                                         'ulciscebantur']}},
                'infinitive': 'ulcisci',
                'konjugation': 'konsonantische Konjugation',
                'perfekt': {'active': {'conjunctive': [None, None, None, None, None, None],
                                       'indicative': [None, None, None, None, None, None]},
                            'passive': {'conjunctive': ['ultus sim',
                                                        'ultus sis',
                                                        'ultus sit',
                                                        'ulti simus',
                                                        'ulti sitis',
                                                        'ulti sint'],
                                        'indicative': ['ultus sum',
                                                       'ultus es',
                                                       'ultus est',
                                                       'ulti sumus',
                                                       'ulti estis',
                                                       'ulti sunt']}},
                'plusquamperfekt': {'active': {'conjunctive': [None,
                                                               None,
                                                               None,
                                                               None,
                                                               None,
                                                               None],
                                               'indicative': [None,
                                                              None,
                                                              None,
                                                              None,
                                                              None,
                                                              None]},
                                    'passive': {'conjunctive': ['ultus essem',
                                                                'ultus esses',
                                                                'ultus esset',
                                                                'ulti essemus',
                                                                'ulti essetis',
                                                                'ulti essent'],
                                                'indicative': ['ultus eram',
                                                               'ultus eras',
                                                               'ultus erat',
                                                               'ulti eramus',
                                                               'ulti eratis',
                                                               'ulti erant']}},
                'ppp': 'ultus',
                'praesens': {'active': {'conjunctive': ['ulciscam',
                                                        'ulciscas',
                                                        'ulciscat',
                                                        'ulciscamus',
                                                        'ulciscatis',
                                                        'ulciscant'],
                                        'indicative': ['ulcisco',
                                                       'ulciscis',
                                                       'ulciscit',
                                                       'ulciscimus',
                                                       'ulciscitis',
                                                       'ulciscunt']},
                             'passive': {'conjunctive': ['ulciscar',
                                                         ['ulciscaris', 'ulciscare'],
                                                         'ulciscatur',
                                                         'ulciscamur',
                                                         'ulciscamini',
                                                         'ulciscantur'],
                                         'indicative': ['ulciscor',
                                                        ['ulcisceris', 'ulciscere'],
                                                        'ulciscitur',
                                                        'ulciscimur',
                                                        'ulciscimini',
                                                        'ulciscuntur']}},
                'translations': ['rächen', 'sich rächen', 'sich rächen (an/für)', 'strafen']}

    result = rip.transform_verb_to_json(rip.transform_verb_forms_to_json(DATA_FORMS),
                                        DATA_INFORMATION)

    assert result == EXPECTED
