# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, matcher, fail

## INNER
# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
_simple = "SENT"
_inverted_question = fail
"""Clause introduced by a (possibly empty) subordinating conjunction."""
_subordinated = "Ssub"
_direct_question = fail
_inverted_declarative = fail
_noun_phrase = "NP"
_wh_noun_phrase = "WHNP"

_interjection = fail
_particle = fail
_adjetival_phrase = "AP"
_verb_phrase = "VN"
_location_constituent = fail
#_adverb_phrase = "AdP"

#
clauses = list_checker((_simple, _subordinated, _direct_question, _inverted_declarative, _inverted_question))
#mention_constituents = list_checker((_noun_phrase, _wh_noun_phrase))
mention_constituents = matcher("NP.*|WHNP")
ner_constituent = list_checker((_location_constituent,))
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = equality_checker(_verb_phrase)

particle_constituents = equality_checker(_particle)
past_participle_verb = equality_checker("VBN")

interjections = equality_checker(_interjection)
simple_or_sub_phrase = list_checker((_simple, _subordinated))

root= list_checker(("root", "top", "ROOT", "TOP"))
