# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

personal_pronoun = "PRP"
possessive_pronoun = "PRP$"
wh_pronoun = "WP"
wh_possessive_pronoun = "WP$"

noun = "NN"
noun_plural = "NNS"

proper_noun = "NNP"
proper_noun_plural = "NNPS"

personal_pronouns = (personal_pronoun, possessive_pronoun)
relative_pronouns = (wh_pronoun, wh_possessive_pronoun)

pronouns = (personal_pronoun, possessive_pronoun, wh_pronoun, wh_possessive_pronoun)

nouns = (noun, noun_plural)
proper_nouns = (proper_noun, proper_noun_plural)

all_nouns = nouns + proper_nouns

adjective = "JJ"
adjective_comparative = "JJR"
adjective_superlative = "JJS"

adjetives = (adjective, adjective_comparative, adjective_superlative)
mod_forms = nouns, adjetives







conjuntion = "CC"

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
