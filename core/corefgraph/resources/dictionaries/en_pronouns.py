# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/14/13'


plural = ("we", "us", "ourself", "ourselves", "ours", "our",  "yourselves", "they", "them", "themselves", "theirs", "their")
singular = ("i", "me", "myself", "mine", "my", "yourself", "he", "him", "himself", "his", "she", "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's")
female = ("her", "hers", "herself", "she")
male = ("he", "him", "himself", "his")
neutral = ("it", "its", "itself", "where", "here", "there", "which")

animate = ("i", "me", "myself", "mine", "my", "we", "us", "yourself", "ourselves", "ours", "our", "you", "yourself", "yours", "your", "yourselves", "he", "him", "himself", "his", "she", "her", "herself", "hers", "her", "one", "oneself", "one's", "they", "them", "themselves", "themselves", "theirs", "their", "they", "them", "'em", "themselves", "who", "whom", "whose")

inanimate = ("it", "itself", "its", "where", "when", "which", "here", "there")

indefinite = ("another", "anybody", "anyone", "anything", "each", "either", "enough", "everybody", "everyone", "everything", "less", "little", "much", "neither", "no one", "nobody", "nothing", "one", "other", "plenty", "somebody", "someone", "something", "both", "few", "fewer", "many", "others", "several", "all", "any", "more", "most", "none", "some", "such")

relative = ("that", "who", "which", "whom", "where", "whose")

reflexive = ("myself", "yourself", "yourselves", "himself", "herself", "itself", "ourselves", "themselves", "oneself")

no_organization = ("i", "me", "myself", "mine", "my", "yourself", "he", "him", "himself", "his", "she", "her", "herself", "hers", "here")

third_person = ("he", "him", "himself", "his", "she", "her", "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's", "they", "them", "themself", "themselves", "theirs", "their", "they", "them", "'em", "themselves")

second_person = ("you", "yourself", "yours", "your", "yourselves")
first_person = ("i", "me", "myself", "mine", "my", "we", "us", "ourself", "ourselves", "ours", "our")
others = ("who", "whom", "whose", "where", "when", "which")


all = set(first_person + second_person + third_person + others)
pleonastic = ("it",)
