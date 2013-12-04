# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

stop_words = set(("un", "une", "uns", "unes", "le", "la", "les", "de", "à", "on", "sur", "dans", "hors", "si", "tel", "ou", "et", "ceux", "cette", "ces", "que", "pour", "est", "était", "suis", "sont", "l'"))

extended_stop_words = (("un","un"))

#non_words = ("mm", "hmm", "ahem", "um")

non_words = ("",)

invalid_stop_words = ("there", "ltd.", "etc", "'s", "hmm")
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

location_modifiers = ("east", "west", "north", "south", "eastern", "western", "northern", "southern", "upper", "lower")
