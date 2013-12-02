# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


stop_words = set(('de', 'en', 'van', 'ik', 'te', 'dat', 'die', 'in', 'een', 'hij',
'het', 'niet', 'zijn', 'is', 'was', 'op', 'aan', 'met', 'als', 'voor', 'had', 'er', 'maar',
'om', 'hem', 'dan', 'zou', 'of', 'wat', 'mijn', 'men', 'dit', 'zo', 'door', 'over', 'ze',
'zich', 'bij', 'ook', 'tot', 'je', 'mij', 'uit', 'der', 'daar', 'haar', 'naar', 'heb', 'hoe', 'heeft',
'hebben', 'deze', 'u', 'want', 'nog', 'zal', 'me', 'zij', 'nu', 'ge', 'geen', 'omdat', 'iets', 'worden', 'toch',
'al', 'waren', 'veel', 'meer', 'doen', 'toen', 'moet', 'ben', 'zonder', 'kan', 'hun', 'dus', 'alles', 'onder', 'ja',
'eens', 'hier', 'wie', 'werd', 'altijd', 'doch', 'wordt', 'wezen', 'kunnen', 'ons', 'zelf', 'tegen', 'na', 'reeds',
'wil', 'kon', 'niets', 'uw', 'iemand', 'geweest', 'andere'))

non_words = ("mm", "hmm", "ahem", "um")
invalid_stop_words = ("there", "ltd.", "etc", "'s", "hmm")
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

location_modifiers = ("east", "west", "north", "south",
                              "eastern", "western", "northern", "southern", "upper", "lower")
