# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

personal_pronoun = "PPER"
possessive_pronoun = "PPOS"
wh_pronoun = "PWS" #Also PWAT
wh_possessive_pronoun = "PWAV"
verbs_list = ("VB", "VBG","VBN")
noun = "NN"
noun_plural = "NN"

proper_noun = "NE"
proper_noun_plural = "NE"

adjective = "ADJA" #Also ADJD
adjective_comparative = "ADJD"
adjective_superlative = "ADJD"

conjunctions = ("KON",) ##Also KOUS KOUI and KOKOM

adjetives = list_checker((adjective, adjective_comparative, adjective_superlative))

personal_pronouns = list_checker((personal_pronoun, possessive_pronoun))
relative_pronouns = list_checker((wh_pronoun, wh_possessive_pronoun, 'PWAT'))

pronouns = list_checker((personal_pronoun, possessive_pronoun, wh_pronoun, wh_possessive_pronoun))

singular_noun = equality_checker("NN")
proper_nouns = list_checker((proper_noun, proper_noun_plural))
nouns = list_checker((noun, noun_plural))

all_nouns = lambda x: nouns(x) or proper_nouns(x)

indefinite = fail

verbs = list_checker(verbs_list)
mod_forms = lambda x: nouns(x) or adjetives(x)

mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)

enumerable_mention_words = list_checker(("NE", "NE"))
conjunction = equality_checker(conjunctions)

bare_plural = "NN"

head_rules = "NN", "NE"
