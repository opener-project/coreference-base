# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

_personal_pronoun = "VNW(pers)" #"PRP"
_possessive_pronoun = "VNW(bez)" #"PRP$"
_wh_pronoun = "VNW(vb)"
_wh_possessive_pronoun = "VNW(vb)"
_wh_determiner = fail
_wh_adverb = fail
_verbs_list= ("WW(pv)","WW(vd)","WW(inf)")
_modal = fail
_noun = "N(soort)"
_noun_plural = "N(soort,mv)"
_interjection = fail
_proper_noun = "N(eigen)"
_proper_noun_plural = "N(eigen,mv)"

_adjective = "ADJ(basis)"
_adjective_comparative = "ADJ(comp)"
_adjective_superlative = "ADJ(sup)"

_conjunctions = ("VG(neven)",)


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

# Enumerations
enumerable_mention_words = list_checker((_proper_noun, "NML"))

conjunction = equality_checker(_conjunctions)
interjections = equality_checker(_interjection)
cardinal = equality_checker("CD")
wh_words = list_checker((_wh_pronoun, _wh_possessive_pronoun, _wh_determiner, _wh_adverb))


head_rules = "noun", "name"


"""
CC - Coordinating conjunction
CD - Cardinal number
DT - Determiner
EX - Existential there
FW - Foreign word
IN - Preposition or subordinating conjunction
JJ - Adjective
JJR - Adjective, comparative
JJS - Adjective, superlative
LS - List item marker
MD - Modal
NN - Noun, singular or mass
NNS - Noun, plural

NNPS - Proper noun, plural
PDT - Predeterminer
POS - Possessive ending
RB - Adverb
RBR - Adverb, comparative
RBS - Adverb, superlative
RP - Particle
SYM - Symbol
TO - to
UH - Interjection
VB - Verb, base form
VBD - Verb, past tense
VBG - Verb, gerund or present participle
VBN - Verb, past participle
VBP - Verb, non-3rd person singular present
VBZ - Verb, 3rd person singular present
WDT - Wh-determiner
WRB - Wh-adverb
"""
