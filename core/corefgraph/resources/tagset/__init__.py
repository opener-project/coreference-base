# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ... import properties

pos_tags = __import__(properties.pos_tag_set + "_pos", globals=globals(), locals=locals())
constituent_tags = __import__(properties.constituent_tag_set + "_constituent", globals=globals(), locals=locals())
ner_tags = __import__(properties.ner_tag_set + "_ner", globals=globals(), locals=locals())
dependency_tags = __import__(properties.dep_tag_set + "_dep", globals=globals(), locals=locals())