# coding=utf-8
"""
This file contains all the element that must be customized for use a specific tag set in hte system. These element must
contains at least:

 * feature detection element
 ** female
 ** male
 ** neutral
 ** singular
 *

The elements that this file publish are any python element(lambda,funtion, object...) that complaint this usage model:

if element_name("PartOfSpeech"):

for example:

plural = lambda pos: pos.endswith("S")

"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'



from resources.lambdas import equality_checker, list_checker, fail, matcher

# http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html

# Determiner

indefinite_determiners = matcher("DI....")

#pronouns

indefinite_pronouns = matcher(r"PI......")

relative_pronouns = matcher(r"PR......")

personal_pronouns = matcher(r"PP......")

pronouns = matcher(r"P.......")

# Pronouns that denotes a mention
mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)
#Nouns

common_nouns = matcher(r"NC.....")
proper_nouns = matcher(r"NP.....")
singular_noun = matcher(r"N..S...")

all_nouns = matcher(r"N......")

# Adjectives
adjectives = matcher(r"A.....")

conjunction = matcher(r"CS")

# Complex questions

female = matcher(r"[AD]..F..|N.F....|V.....F|P..F....")

male = matcher(r"[AD]..M..|N.M....|V.....M|P.M.....|S..M.]")

neutral = matcher(r"[AD]..N..|P..N....")

singular = matcher(r"[AD]...S.|N..S...|V....S.|P...S..|S...S")

plural = matcher(r"[AD]...P.|N..P...|V....P.|P...P..")

mod_forms = lambda x: common_nouns(x) or adjectives(x)

indefinite = lambda x: indefinite_determiners(x) or indefinite_pronouns(x)

#indefinite_articles = lambda x: indefinite_determiners(x) or indefinite_pronouns(x)


enumerable_mention_words = lambda x: proper_nouns(x)

#TODO RODRIGO
head_rules = "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"


# Trash Zone
#adverbs = itertools.product("R", "GN")
#determiner = itertools.product("D", "DPTEIA", "0123", "MFCN", "SPN", "SP0")
#interjection = "I"
#verbs = expand("V", "MAS", "ISMNGP", "PIFSC0", "0123", "SP0", "MF0")
#prepositions = expand(("SP",), "SC0", "MS0")
#punctuation = "F"
#number = expand("Z", "DMPU0")
#date = "W"
#demostrative_pronouns = expand(("PD0",), "MFCN", "SP", ("000",))
#possessive_pronouns = expand(("PX",), "123", "MFC", "SPN", "0", "SP0", "0")

#interrogative_pronouns = expand(("PT0",), "MFC0", ("000",))

#exclamative_pronoun = "PE000000"


