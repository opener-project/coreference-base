# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


stop_words = set(("a", "an", "the", "of", "at", "on", "upon", "in", "to", "from", "out", "as", "so", "such", "or",
    "and", "those", "this", "these", "that", "for", ",", "is", "was", "am", "are", "'s", "been", "were"
    ))

extended_stop_words = set(("the", "this", "mr.", "miss", "mrs.", "dr.", "ms.", "inc.", "ltd.", "corp.", "'s"))
# all pronouns are added to stop_word

non_words = ("mm", "hmm", "ahem", "um")

invalid_stop_words = ("u.s.", "u.k", "u.s.s.r.", "there", "ltd.")
invalid_start_words = ("'s",)
invalid_end_words = ("etc.", )

location_modifiers = ("east", "west", "north", "south",
                              "eastern", "western", "northern", "southern", "upper", "lower")
