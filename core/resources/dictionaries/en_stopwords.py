# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


stop_words = set(("a", "an", "the", "of", "at", "on", "upon", "in", "to", "from", "out", "as", "so", "such", "or",
    "and", "those", "this", "these", "that", "for", ",", "is", "was", "am", "are", "'s", "been", "were"
    ))

non_words = ("mm", "hmm", "ahem", "um")

invalid_stop_words = ("u.s.", "u.k", "u.s.s.r.", "there", "ltd.")
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

temporals = ("second", "minute", "hour", "day", "week", "month", "year", "decade", "century", "millennium",
      "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "now",
      "yesterday", "tomorrow", "age", "time", "era", "epoch", "morning", "evening", "day", "night", "noon", "afternoon",
      "semester", "trimester", "quarter", "term", "winter", "spring", "summer", "fall", "autumn", "season",
      "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
