# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from ..lambdas import equality_checker, list_checker, fail

personal_pronoun = "pron" #"PRP"
possessive_pronoun = "det" #"PRP$"
wh_pronoun = "pron"
wh_possessive_pronoun = "det"
verbs_list= ("VB","VB","VB")
noun = "noun"
noun_plural = "noun"

proper_noun = "name"
proper_noun_plural = "name"

adjective = "adj"
adjective_comparative = "adj"
adjective_superlative = "adj"

conjunctions = ("CC",)

adjetives = list_checker((adjective, adjective_comparative, adjective_superlative))

personal_pronouns = list_checker((personal_pronoun, possessive_pronoun))
relative_pronouns = list_checker((wh_pronoun, wh_possessive_pronoun))

pronouns = list_checker((personal_pronoun, possessive_pronoun, wh_pronoun, wh_possessive_pronoun))

singular_noun = equality_checker("noun")
proper_nouns = list_checker((proper_noun, proper_noun_plural))
nouns = list_checker((noun, noun_plural))
all_nouns = lambda x: nouns(x) or proper_nouns(x)

indefinite = fail

verbs = list_checker(verbs_list)
mod_forms = lambda x: nouns(x) or adjetives(x)

mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)

enumerable_mention_words = list_checker(("name","name"))
conjuntion = equality_checker("vg")

bare_plural= "noun"
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
