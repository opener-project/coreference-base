# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from resources.lambdas import equality_checker, list_checker

# Clauses

""" simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a
wh-word and that does not exhibit subject-verb inversion"""
simple = "smain"

"""Clause introduced by a (possibly empty) subordinating conjunction."""
subordinated = "ssub"

"""Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be
bracketed as SBAR, not SBARQ."""
direct_question = "whq"   #"SBARQ"

"""Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal."""
inverted_declarative = "sv1" #SINV

"""Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ."""
inverted_question = "sv1" # SQ

# Phrases

noun_phrase = "np"
wh_noun_phrase = "np"

adjetival_phrase = "ap"
adverb_phrase = "advp"
conjuntion_phrase = "conj"
fragment = "du"
interjection = "du"
list_marker = "" # "LST"
not_a_constituent = "du"
noun_phrase_mark = "np"
prepositional_phrase = "pp"
parenthetical = ""
particle = ""  #"PRT"
quantifier_phrase = "np"  # QP"
reduced_relative_clause = ""  #"RRC"
unlike_coordinated_phrase = "" #"UCP"
verb_phrase = "smain"  #"VP"
wh_adjective_phrase = "whq" #"WHADJP"
wh_adverb = "whq"  ##" WHAVP"
wh_prepositional_phrase = "whq"
unknown = "X"

clauses = list_checker((simple, subordinated, direct_question, inverted_declarative, inverted_question))
verb_phrases = equality_checker(verb_phrase)
noun_phrases = equality_checker(noun_phrase)

mention_constituents = list_checker((noun_phrase, wh_noun_phrase))
phrases = list_checker((noun_phrase, wh_noun_phrase, adjetival_phrase, adverb_phrase, conjuntion_phrase, fragment, interjection, list_marker,
    not_a_constituent, noun_phrase_mark, prepositional_phrase, parenthetical, particle, quantifier_phrase,
    reduced_relative_clause, unlike_coordinated_phrase, verb_phrase, wh_adjective_phrase, wh_adverb,
    wh_prepositional_phrase, unknown))
