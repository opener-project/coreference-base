# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


#stop_words = set(("a", "an", "the", "of", "at", "on", "upon", "in", "to", "from", "out", "as", "so", "such", "or",
#    "and", "those", "this", "these", "that", "for", ",", "is", "was", "am", "are", "'s", "been", "were"
#    ))

stop_words = set(("un", "une", "uns", "unes", "le", "la", "les", "de", "à", "on", "sur", "dans", "hors", "si", "tel", "ou", "et", "ceux", "cette",
    "ces", "que", "pour", "est", "était", "suis", "sont", "l'"))

#non_words = ("mm", "hmm", "ahem", "um")

non_words = ()

invalid_stop_words = ("there", "ltd.", "etc", "'s", "hmm")
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

location_modifiers = ("east", "west", "north", "south",
                              "eastern", "western", "northern", "southern", "upper", "lower")
