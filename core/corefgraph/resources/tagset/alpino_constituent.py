# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
_simple = "smain"
"""Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ."""
_inverted_question = "sv1" # SQ

"""Clause introduced by a (possibly empty) subordinating conjunction."""
_subordinated = "ssub"

"""Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be
bracketed as SBAR, not SBARQ."""
_direct_question = "whq"   #"SBARQ"

"""Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal."""
_inverted_declarative = "sv1" #SINV


# Phrases

_noun_phrase = "np"
_wh_noun_phrase = "np"

_interjection = "du"
_particle = fail  #"PRT"
_verb_phrase = "smain"  #"VP"
_location_constituent = fail 

#
clauses = list_checker((_simple, _subordinated, _direct_question, _inverted_declarative, _inverted_question))
mention_constituents = list_checker((_noun_phrase,"noun"))
ner_constituent = list_checker((_location_constituent,))
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = equality_checker(_verb_phrase)

particle_constituents = equality_checker(_particle)
past_participle_verb = equality_checker("VBN")

interjections = equality_checker(_interjection)
simple_or_sub_phrase = list_checker((_simple, _subordinated))

root= list_checker(("root", "top", "ROOT", "TOP"))
