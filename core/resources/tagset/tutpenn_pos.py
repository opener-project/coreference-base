# coding=utf-8
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'
__date__ = '5/16/2013'

from resources.lambdas import equality_checker, list_checker, fail

personal_pronoun = "PRO~PE"
possessive_pronoun = "PRO~PO"
wh_pronoun = "PRO~RE" #in TUT there are distinct tags for relative and interrogative pronouns. Here only relative pro are given
#wh_possessive_pronoun = "WP$"
verbs_list = ("VAU~IM","VAU~IN","VAU~RA","VAU~FU","VAU~RE","VAU~CO","VAU~IP","VAU~CG","VAU~GE","VMA~IM","VMA~IN","VMA~RA","VMA~PP","VMA~PA","VMA~FU","VMA~RE","VMA~CO","VMA~CG","VMA~IP","VMO~CG","VMO~CO","VMO~FU","VMO~IM","VMO~RE","VMO~RA","VMO~IP","VMA~GE","VMA~PE")

noun = "NOU~CS" #if we add gender features to the tags in TUT we may need to change here
noun_plural = "NOU~CP" #if we add gender features to the tags in TUT we may need to change here

proper_noun = "NOU~PR"
#proper_noun_plural = "NNPS"

#adjective = "JJ"
#adjective_comparative = "JJR"
#adjective_superlative = "JJS"


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
"""
adjective_qualif = "ADJ~QU"
adjective_ord = "ADJ~OR"
adjective_indef = "ADJ~IN"
adjective_dem = "ADJ~DE"
adjective_poss = "ADJ~PO"
adjective_deitt = "ADJ~DI"
adjective_interr = "ADJ~IR"
adjective_excl = "ADJ~EX"

adjetives = list_checker((adjective_qualif, adjective_ord, adjective_indef, adjective_dem, adjective_poss, adjective_deitt, adjective_interr, adjective_excl))

personal_pronouns = list_checker((personal_pronoun, possessive_pronoun))
#relative_pronouns = (wh_pronoun, wh_possessive_pronoun)
relative_pronouns = list_checker((wh_pronoun, wh_pronoun))

#pronouns = (personal_pronoun, possessive_pronoun, wh_pronoun, wh_possessive_pronoun)
pronouns = list_checker((personal_pronoun, possessive_pronoun, wh_pronoun))

singular_noun = equality_checker(noun)
proper_nouns = list_checker((proper_noun, proper_noun))
nouns = list_checker((noun, noun_plural))
all_nouns = lambda x: nouns(x) or proper_nouns(x)

indefinite = fail

verbs = list_checker(verbs_list)
mod_forms = lambda x: nouns(x) or adjetives(x)

# Pronouns that denote a mention
mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)

# enumerations
enumerable_mention_words = list_checker(("NOU~PR", "NOU~PR"))
conjunction = equality_checker("CONJ")

bare_plural = "NOU~CP"
head_rules = "NOU~CS", "NOU~PR","NOU~CP", "ADJ~PO"

