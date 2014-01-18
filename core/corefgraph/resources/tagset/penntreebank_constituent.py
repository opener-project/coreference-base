# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..lambdas import equality_checker, list_checker

# INNER
_simple = "S"
_inverted_question = "SQ"
_subordinated = "SBAR"
_direct_question = "SBARQ"
_inverted_declarative = "SINV"
_noun_phrase = "NP"
_wh_noun_phrase = "WHNP"

_interjection = "INTJ"
_particle = "PRT"
_verb_phrase = "VP"
_location_constituent = "NML"

#
clauses = list_checker((_simple, _subordinated, _direct_question, _inverted_declarative, _inverted_question))
mention_constituents = list_checker((_noun_phrase, _wh_noun_phrase))
ner_constituent = list_checker((_location_constituent,))
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = equality_checker(_verb_phrase)

particle_constituents = equality_checker(_particle)
past_participle_verb = equality_checker("VBN")

interjections = equality_checker(_interjection)
simple_or_sub_phrase = list_checker((_simple, _subordinated))
root= list_checker(("root", "top", "ROOT", "TOP"))



