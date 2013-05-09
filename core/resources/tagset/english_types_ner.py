# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

# absence of NE type

no_ner = "o"

# Tagset form Ontonotes 4.0 and CoNLL 2003

mention_ner = ("PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART",
                 "LAW", "LANGUAGE", "DATE", "TIME", "MISC")

# we filter NEs of this type as per Stanford instructions

no_mention_ner = ("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")

person_ner_tag = ("PERSON", "PER")


animate = ("person",
              "per")


inanimate = ('facility',
                'norp',
                'location', 'loc',
                'product',
                'event',
                'organization', 'org'
                'work of art',
                'law',
                'language',
                'date',
                'time',
                'percent',
                'money',
                'number',
                'quantity',
                'ordinal',
                'cardinal',
                'misc',
                'veh',
                'fac',
                'gpe',
                'wea',
                )

all = mention_ner + no_mention_ner + person_ner_tag

single_ner = set(all).difference(("org", "organization"))