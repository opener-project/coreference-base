#
# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
list_checker = lambda list: lambda element: element in list
equality_checker = lambda value: lambda element: element == value
## penn treebank similarities
adjetival_phrases = list_checker(("SA", "S.A", "GRUP.A"))
adverb_phrase = equality_checker("SADV")
conjunction_phrase = "COORD"
fragment = "FRAGMENT"
interjection = "INTERJECCIÓ"
list_marker = "F"
#NX = ("SN","GRUP.NOM")
prepositional_phrase = equality_checker("SP")
#Parenthetical not exist
#PRT not exist
reduced_relative_clause = "RELATIU"
# unlike_coordinated_phrase = "COORD"
verb_phrase = "GRUP.VERB"
#wh_adjective_phrase  = ("SA","S.A", "GRUP.A")
#wh_adverb = ("SADV", "GRUP.ADV")
#wh_noun_phrase = ("SN", "GRUP.NOM")
#wh_prepositional_phrase = "SP"
#parenthetical not exist
#particle not exist
#quantifier_phrase not exist


###
#Not from the tagset but may be useful
unknown = "X"

# tagset tags
sentence = "SENTENCE"

infinitive = "INFINITIU"
gerund = "GERUNDI"
participle = "PARTICIPIU"

pronominal_morpheme = "MORFEMA.PRONOMINAL"
verbal_morpheme = "VERBAL.MORFEME"


inserted_element = "INC"
negation = "NEG"
preposition = "PREP"
relative = "RELATIU"
specifier = "SPEC"

# Used tags and clusters

artificial_mention = equality_checker("XMENTION")
clauses = list_checker(("S", "SENTENCE"))
noun_phrases = list_checker(("SN", "GRUP.NOM"))
verb_phrases = list_checker(("GRUP.VERB",))
mention_constituents = lambda x: noun_phrases(x) or artificial_mention(x)
conjunction = list_checker(("CONJ",))
phrases = lambda x: adjetival_phrases(x) or adverb_phrase(x) or prepositional_phrase(x)