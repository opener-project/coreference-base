# coding=utf-8
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'
__date__= '5/16/2013'

from ..lambdas import equality_checker, list_checker, matcher, fail

## INNER 
# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
_simple = "S"

"""Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ."""
_inverted_question = fail

"""Clause introduced by a (possibly empty) subordinating conjunction."""
_subordinated = "SBAR"

"""Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be
bracketed as SBAR, not SBARQ."""
_direct_question = fail

"""Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal."""
_inverted_declarative = fail
_noun_phrase = "NP"
_wh_noun_phrase = "NP"

_interjection = fail
_particle = fail
_verb_phrase = "VP"
_location_constituent = fail

#
clauses = list_checker((_simple, _subordinated, _direct_question, _inverted_declarative, _inverted_question))
mention_constituents = matcher("NP.*")
ner_constituent = list_checker((_location_constituent,))
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = equality_checker(_verb_phrase)

particle_constituents = equality_checker(_particle)
past_participle_verb = equality_checker("VBN")

interjections = equality_checker(_interjection)
simple_or_sub_phrase = list_checker((_simple, _subordinated))

root= list_checker(("root", "top", "ROOT", "TOP"))
