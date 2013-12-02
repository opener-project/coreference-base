# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
_simple = "SENT"

"""Clause introduced by a (possibly empty) subordinating conjunction."""
_subordinated = "Ssub"


# Phrases

_noun_phrase = "NP"
_wh_noun_phrase = "WHNP"

_adjetival_phrase = "AP"
_adverb_phrase = "AdP"
_verb_phrase = "VN"


#
clauses = list_checker((_simple, _subordinated))
mention_constituents = list_checker((_noun_phrase, _wh_noun_phrase))
ner_constituent = fail
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = equality_checker(_verb_phrase)

particle_constituents = fail
past_participle_verb = equality_checker("VBN")

interjections = fail
simple_or_sub_phrase = list_checker((_simple, ))

root= list_checker(("root", "top", "ROOT", "TOP"))
