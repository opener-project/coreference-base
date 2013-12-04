# -*- coding: utf-8 -*-

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/14/13'


#plural = ("we", "us", "ourself", "ourselves", "ours", "our",  "yourselves", "they", "them",
#          "themselves", "theirs", "their")

plural = ("nous", "notre", "nous-mêmes", "nous", "notre", "nos", "vous", "ils", "eux", "en soi", "leur", "leur")

#singular = ("i", "me", "myself", "mine", "my", "yourself", "he", "him", "himself", "his", "she",
#            "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's")

singular = ("Je", "me", "moi", "mien", "mon", "vous", "il", "lui", "elle", "elle-même", "sien", "son", "il", "elle", "un", "soi-même")

#female = ("her", "hers", "herself", "she")

female = ("son", "sien", "elle-même", "elle")

#male = ("he", "him", "himself", "his")

male = ("il", "lui", "lui-même", "son")

#neutral = ("it", "its", "itself", "where", "here", "there", "which")

neutral = ("il", "son", "même", "où", "ici", "il", "qui")

#animate = ("i", "me", "myself", "mine", "my",
#           "we", "us", "yourself", "ourselves", "ours", "our",
#           "you", "yourself", "yours", "your", "yourselves",
#           "he", "him", "himself", "his", "she", "her", "herself", "hers", "her", "one", "oneself", "one's",
#           "they", "them", "themselves", "themselves", "theirs", "their", "they", "them", "'em", "themselves",
#           "who", "whom", "whose")

animate = ("Je", "me", "moi", "mien", "mon", "nous", "notre", "vous", "nous", "notre", "nos", "vous", "vous", "vos", "votre", "vous", "il", "lui", "lui-même", "son", "elle", "elle", "elle", "sien", "son", "un", "soi-même", "ils", "eux", "leur", "ils", "eux", "qui", "qui")

#inanimate = ("it", "itself", "its", "where", "when", "which", "here", "there")

inanimate = ("il", "même", "son", "où", "quand", "qui", "ici", "là-bas")

#indefinite = set(("another", "anybody", "anyone", "anything", "each", "either", "enough", "everybody",
#    "everyone", "everything", "less", "little", "much", "neither", "no one", "nobody",
#    "nothing", "one", "other", "plenty", "somebody", "someone", "something", "both",
#    "few", "fewer", "many", "others", "several", "all", "any", "more", "most", "none",
#    "some", "such"))

indefinite = set(("autre", "quiconque", "quelqu'un", "rien", "chacun", "soit", "assez", "tous", "tout le monde", "tout", "peu", "beaucoup", "ni", "nul", "personne", "rien", "un", "autre", "beaucoup", "quelque chose", "deux", "moins", "autres", "plusieurs", "tout", "une", "plus", "plupart", "none", "certains", "tel"))

#relative = ("that", "who", "which", "whom", "where", "whose")

relative = ("qui", "qui", "où", "que", "cas", "dont")

reflexive = ("ja",)

no_organization = ("ja",)

third_person = ("ja",)

second_person = ("ja",)

first_person = ("ja",)

others = ("who", "whom", "whose", "where", "when", "which")

all = set(first_person + second_person + third_person + others)

pleonastic = ("it",)
