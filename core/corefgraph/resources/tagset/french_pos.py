# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

_personal_pronoun = "PROms"
_possessive_pronoun = "PROms"
_wh_pronoun = "PROms"
_wh_possessive_pronoun = "PROms"
_wh_determiner = fail
_wh_adverb = fail
_verbs_list=("VB",)
_modal = fail
_noun = "NC"
_noun_plural = "NCms"
_interjection = "UH"
_proper_noun = "NNP"
_proper_noun_plural = "NCmp"

_adjective = "Ams"
# No equivalent in french tagging? And what about gender? There is no variable for gender pos
_adjective_comparative = fail
_adjective_superlative = fail


_conjunctions = fail
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

#TODO Adapt to semantic heads

head_rules = "NC", "NNP", "NCms"

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
