# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..lambdas import list_checker, equality_checker, fail

_artificial_mention = equality_checker("XMENTION")

clauses = list_checker(("S", "SENTENCE"))
mention_constituents = lambda x: noun_phrases(x) or _artificial_mention(x)
ner_constituent = fail
noun_phrases = list_checker(("SN", "GRUP.NOM"))
verb_phrases = list_checker(("GRUP.VERB",))

particle_constituents = fail
past_participle_verb = fail

interjections = equality_checker("INTERJECCIÓ")
simple_or_sub_phrase = clauses
root = list_checker(("root", "top", "ROOT", "TOP"))
