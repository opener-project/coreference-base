# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


list_checker = lambda list: lambda element: element in list
equality_checker = lambda value: lambda element: element == value

# NE tag for no named entity elements
no_ner = "O"

# NE types that denotes mention
mention_ner = list_checker(("PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART",
                 "LAW", "LANGUAGE", "DATE", "TIME"))

# NE types that must be filtered from mention candidates
no_mention_ner = list_checker(("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"))

# NE tags for persons
person = list_checker(("PERSON", "PER"))
organization = list_checker(("ORG", "ORGANIZATION"))
# NE tags that denotes animacy
animate = person

inanimate = list_checker(("FACILITY", "NORP", "LOCATION", "LOC", "PRODUCT", "EVENT", "ORGANIZATION", "ORG", "WORK OF ART", "LAW",
             "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "NUMBER", "QUANTITY", "ORDINAL", "CARDINAL", "MISC",
             "VEH", "FAC", "GPE", "WEA"))
all = lambda x: mention_ner(x) or no_mention_ner(x)