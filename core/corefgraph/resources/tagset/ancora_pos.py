# coding=utf-8
# http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html
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

verb = lambda pos: pos.startswith("V")

"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..lambdas import equality_checker, list_checker, fail, matcher


# INNER USAGE
_indefinite_determiners = matcher("DI....")
_indefinite_pronouns = matcher(r"PI......")
# END OF INNER USAGE

# features questions
female = matcher(r"[AD]..F..|N.F....|V.....F|P..F....")

male = matcher(r"[AD]..M..|N.M....|V.....M|P.M.....|S..M.]")

neutral = matcher(r"[AD]..N..|P..N....")

singular = matcher(r"[AD]...S.|N..S...|V....S.|P...S..|S...S")

plural = matcher(r"[AD]...P.|N..P...|V....P.|P...P..")

#Adecjtives
adjectives = matcher(r"A.....")

#pronouns
personal_pronouns = matcher(r"PP.+")
relative_pronouns = matcher(r"PR.+")
pronouns = matcher(r"P.+")
mention_pronouns = lambda x: relative_pronouns(x) or personal_pronouns(x)

#Nouns
singular_common_noun = matcher(r"NC.S.+")
plural_common_noun = matcher(r"NC.P.+")
proper_nouns = matcher(r"NP.+")
all_nouns = matcher(r"N.+")

#Verbs
verbs = matcher(r"V.+")
modals = fail
mod_forms = lambda x: singular_common_noun(x) or plural_common_noun(x) or adjectives(x) or verbs(x) or cardinal(x)
indefinite = lambda x: _indefinite_determiners(x) or _indefinite_pronouns(x)

# Others
enumerable_mention_words = lambda x: proper_nouns(x)
conjunction = matcher(r"CS")
interjections = equality_checker("I")
cardinal = matcher("Z.+")
#TODO TALK WITH RODRIGO
wh_words = relative_pronouns

#TODO RODRIGO
head_rules = "NN", "NNP", "NNPS", "NNS", "NX", "JJR", "POS"
