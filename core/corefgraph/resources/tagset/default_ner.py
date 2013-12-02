# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


from ..lambdas import list_checker


no_ner = "O"
other = "MISC"

person = list_checker(("PERSON", "PER"))
organization = list_checker(("ORG", "ORGANIZATION"))

# NE types that denote mention
mention_ner = list_checker(("PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "NML", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART",
                            "LAW", "LANGUAGE", "DATE", "TIME"))

# NE types that must be filtered from mention candidates
no_mention_ner = list_checker(("PERCENT", "MONEY", "QUANTITY",  "CARDINAL","ORDINAL", "DATE"))

# NE tags that denote animacy
inanimate = list_checker(("FACILITY", "NORP", "LOCATION", "LOC", "PRODUCT", "EVENT", "ORGANIZATION", "ORG", "WORK OF ART", "LAW",
                         "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "NUMBER", "QUANTITY", "ORDINAL", "CARDINAL", "MISC",
                         "VEH", "FAC", "GPE", "WEA", "NML"))
animate = person

# NE tags for person
all = lambda x: mention_ner(x) or no_mention_ner(x)
