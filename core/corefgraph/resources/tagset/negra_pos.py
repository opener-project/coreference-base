# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

_personal_pronoun = "PPER"
_possessive_pronoun = "PPOS"
_wh_pronoun = "PWS" #Also PWAT
_wh_possessive_pronoun = "PWAV"
_wh_determiner = fail
_wh_adverb = fail
_verbs_list = ("VB", "VBG","VBN")
_modal = fail
_noun = "NN"
_noun_plural = "NN"
_interjection = "ITJ"
_proper_noun = "NE"
_proper_noun_plural = "NE"

_adjective = "ADJA" #Also ADJD
_adjective_comparative = "ADJD"
_adjective_superlative = "ADJD"

_conjunctions = ("KON",) ##Also KOUS KOUI and KOKOM

# features questions

female = fail
male = fail
neutral = fail
singular = fail

adjectives = list_checker((_adjective, _adjective_comparative, _adjective_superlative))


#pronouns
personal_pronouns = list_checker((_personal_pronoun, _possessive_pronoun))
relative_pronouns = list_checker((_wh_pronoun, _wh_possessive_pronoun, 'PWAT'))
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

enumerable_mention_words = list_checker(("NE", "NE"))

conjunction = equality_checker(_conjunctions)
interjections = equality_checker(_interjection)
cardinal = equality_checker("CD")
wh_words = list_checker((_wh_pronoun, _wh_possessive_pronoun, _wh_determiner, _wh_adverb))

head_rules = "NN", "NE"
