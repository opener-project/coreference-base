# coding=utf-8
""" Penntreebank POS tag checkers.

Each elements in this module is a function that check if a POS tag.

Elements starting with _ is only for internal use.
"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..lambdas import equality_checker, list_checker, fail


# Inner usage only
_personal_pronoun = "PRP"
_possessive_pronoun = "PRP$"
_wh_pronoun = "WP"
_wh_possessive_pronoun = "WP$"
_wh_determiner = "WDT"
_wh_adverb = "WRB"
_verbs_list = ("VB", "VB", "VBG", "VBN", "VBP ", "VBZ")
_modal = "MD"
_noun = "NN"
_noun_plural = "NNS"
_interjection = "UH"
_proper_noun = "NNP"
_proper_noun_plural = "NNPS"

_adjective = "JJ"
_adjective_comparative = "JJR"
_adjective_superlative = "JJS"

_conjunctions = ("CC",)

#comma = equality_checker(",")

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
head_rules = "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"
