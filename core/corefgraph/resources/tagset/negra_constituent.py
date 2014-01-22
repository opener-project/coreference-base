# coding=utf-8
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'

from ..lambdas import equality_checker, list_checker, matcher, fail

## INNER 
# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
_simple = "S"

"""Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ."""
_inverted_question = "S"

"""Clause introduced by a (possibly empty) subordinating conjunction."""
_subordinated = "S" #also OC

"""Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be
bracketed as SBAR, not SBARQ."""
_direct_question = "S"

"""Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal."""
_inverted_declarative = "S"

_noun_phrase = matcher("NP.*")
_wh_noun_phrase = matcher("NP.*")

_interjection = "ITJ"
_particle = "PTKZU"  #Also  PTKNEG, PTVZ, PTKSNT, PTKA
_verb_phrase = "VP"  # Also VZ
_location_constituent = fail

#
clauses = list_checker((_simple,"OC", _subordinated, _direct_question, _inverted_declarative, _inverted_question))
mention_constituents = matcher("C?NP.*|MPN")
ner_constituent = list_checker((_location_constituent,))
noun_phrases = equality_checker(_noun_phrase)
verb_phrases = list_checker((_verb_phrase,"VZ"))

particle_constituents = list_checker(("PTKZU","PTKNEG","PTVZ","PTKSNT","PTKA"))
past_participle_verb = equality_checker("VBN")

interjections = equality_checker(_interjection)
simple_or_sub_phrase = list_checker((_simple, _subordinated))

root= list_checker(("root", "top", "ROOT", "TOP"))
