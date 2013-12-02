# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail


# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
simple = "S"

"""Clause introduced by a (possibly empty) subordinating conjunction."""
subordinated = "S" #also OC

"""Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be
bracketed as SBAR, not SBARQ."""
direct_question = "S"

"""Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal."""
inverted_declarative = "S"

"""Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ."""
inverted_question = "S"

clauses = list_checker((simple, subordinated, direct_question, inverted_declarative, inverted_question,'OC','RC'))


# Phrases

noun_phrase = "NP"
wh_noun_phrase = "NP"

adjetival_phrase = "AP"
adverb_phrase = "AVP"
conjuntion_phrase = "CAP" #Also CAVP CO
fragment = "?"
interjection = "ITJ"
list_marker = "?"
not_a_constituent = "?"
noun_phrase_mark = "?"
prepositional_phrase = "PP"
parenthetical = "?"
particle = "PTKZU"  #Also  PTKNEG, PTVZ, PTKSNT, PTKA
quantifier_phrase = "QP"
reduced_relative_clause = "RC"
unlike_coordinated_phrase = "?"
verb_phrase = "VP"  # Also VZ
wh_adjective_phrase = "AP" #"WHADJP"
wh_adverb = "AVP"  ##" WHAVP"
wh_prepositional_phrase = "PP"
unknown = "QL"

verb_phrases = equality_checker(verb_phrase)
noun_phrases = equality_checker(noun_phrase)

mention_constituents = list_checker((noun_phrase, wh_noun_phrase))

phrases = (noun_phrase, wh_noun_phrase, adjetival_phrase, adverb_phrase, conjuntion_phrase, fragment, interjection, list_marker,
    not_a_constituent, noun_phrase_mark, prepositional_phrase, parenthetical, particle, quantifier_phrase,
    reduced_relative_clause, unlike_coordinated_phrase, verb_phrase, wh_adjective_phrase, wh_adverb,
    wh_prepositional_phrase, unknown,'CAVP','CO','PTKNEG', 'PTVZ', 'PTKSNT', 'PTKA')


root= list_checker(("root", "top", "ROOT", "TOP"))
