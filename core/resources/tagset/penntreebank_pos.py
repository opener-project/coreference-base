# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from resources.lambdas import equality_checker, list_checker, fail

personal_pronoun = "PRP"
possessive_pronoun = "PRP$"
wh_pronoun = "WP"
wh_possessive_pronoun = "WP$"
verbs_list = ("VB", "VB", "VBG", "VBN", "VBP ", "VBZ")
noun = "NN"
noun_plural = "NNS"

proper_noun = "NNP"
proper_noun_plural = "NNPS"



adjective = "JJ"
adjective_comparative = "JJR"
adjective_superlative = "JJS"

conjunctions = ("CC",)


adjetives = list_checker((adjective, adjective_comparative, adjective_superlative))

personal_pronouns = list_checker((personal_pronoun, possessive_pronoun))
relative_pronouns = list_checker((wh_pronoun, wh_possessive_pronoun))

pronouns = list_checker((personal_pronoun, possessive_pronoun, wh_pronoun, wh_possessive_pronoun))

singular_noun = equality_checker("NNS")
proper_nouns = list_checker((proper_noun, proper_noun_plural))
nouns = list_checker((noun, noun_plural))
all_nouns = lambda x: nouns(x) or proper_nouns(x)

indefinite = fail

verbs = list_checker(verbs_list)
mod_forms = lambda x: nouns(x) or adjetives(x)

# Pronouns that denotes a mention
mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)

# Enumerations
enumerable_mention_words = list_checker(("NNP", "NML"))
conjunction = equality_checker(conjunctions)

bare_plural = "NNS"
#TODO Adapt to semantic heads
head_rules = "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"
