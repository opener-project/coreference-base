# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

no_ner = "o"

mention_ner = ("PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART",
                 "LAW", "LANGUAGE", "DATE", "TIME")

no_mention_ner = ("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
person_ner_tag = ("PERSON", "PER")

all = mention_ner + no_mention_ner + person_ner_tag