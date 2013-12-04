# coding=utf-8
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'
__date__ = '5/16/2013'

from ..lambdas import equality_checker, list_checker, fail

_personal_pronoun = "PRO~PE"
_possessive_pronoun = "PRO~PO"
_wh_pronoun = "PRO~RE" #in TUT there are distinct tags for relative and interrogative pronouns. Here only relative pro are given
_wh_possessive_pronoun = fail
_wh_determiner = fail
_wh_adverb = fail
_verbs_list =("VAU~CG","VAU~CO","VAU~FU","VAU~IM","VAU~IN","VAU~PA","VAU~RA","VAU~RE","VMA~CG","VMA~CO","VMA~FU","VMA~GE","VMA~IM","VMA~IN","VMA~IP","VMA~PA","VMA~PE","VMA~RA","VMA~RE","VMO~CG","VMO~CO","VMO~FU","VMO~GE","VMO~IM","VMO~IN","VMO~PA","VMO~RA","VMO~RE")
_modal = fail
_noun = "NOU~CS" #if we add gender features to the tags in TUT we may need to change here
_noun_plural = "NOU~CP" #if we add gender features to the tags in TUT we may need to change here
_interjection = fail
_proper_noun = "NOU~PR"
_proper_noun_plural = fail

_adjective = "ADJ~QU"
_adjective_comparative = "ADJ~QU"
_adjective_superlative = "ADJ~QU"

"""Adjectives
TUT does not have tags for comparative and superlative, but make finer distinctions for the different kinds of adjectives:
ADJ~QU : qualifying adjective
ADJ~OR : ordinal adjective
ADJ~IN : indefinite adjective
ADJ~DE : demonstrative adjective
ADJ~PO : possessive adjective
ADJ~DI : deictic adjective
ADJ~IR : interrogative adjective
ADJ~EX : exclamative adjective

following lines modified accordingly
TODO check correctedness
adjective_qualif = "ADJ~QU"
adjective_ord = "ADJ~OR"
adjective_indef = "ADJ~IN"
adjective_dem = "ADJ~DE"
adjective_poss = "ADJ~PO"
adjective_deitt = "ADJ~DI"
adjective_interr = "ADJ~IR"
adjective_excl = "ADJ~EX"
"""

_conjunctions = equality_checker("CONJ",)

# Usable functions

# features questions

female = fail
male = fail
neutral = fail
singular = fail

#Adjectives
adjectives = list_checker((_adjective, _adjective_comparative, _adjective_superlative))

#pronouns
personal_pronouns = list_checker((_personal_pronoun, _possessive_pronoun))
relative_pronouns = list_checker((_wh_pronoun, _wh_possessive_pronoun))
pronouns = list_checker((_personal_pronoun, _possessive_pronoun, _wh_pronoun, _wh_possessive_pronoun))
mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)


singular_common_noun = equality_checker(_noun)
plural_common_noun = equality_checker(_noun_plural)
proper_nouns = list_checker((_proper_noun, _proper_noun_plural))
all_nouns = lambda x: singular_common_noun(x) or plural_common_noun(x) or proper_nouns(x)

verbs = list_checker(_verbs_list)
modals = equality_checker(_modal)
mod_forms = lambda x: singular_common_noun(x) or plural_common_noun(x) or adjectives(x) or verbs(x) or cardinal(x)
indefinite = fail

# enumerations
enumerable_mention_words = list_checker(("NOU~PR", "NOU~PR"))

conjunction = equality_checker(_conjunctions)
interjections = equality_checker(_interjection)
cardinal = equality_checker("CD")
wh_words = list_checker((_wh_pronoun, _wh_possessive_pronoun, _wh_determiner, _wh_adverb))

head_rules = "NOU~CS", "NOU~PR","NOU~CP", "ADJ~PO"

