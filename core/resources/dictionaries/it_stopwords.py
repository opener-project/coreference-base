# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'

#very basic stopword list.

stop_words = set(("﻿a", "ad", "ai", "al", "alla", "allo", "con", "cosi'", "così", "da", "del", "della", "dello", "dentro", "di", "e", "ecco", "ed", "fra", "fuori", "ha", "hai", "hanno", "ho", "il", "in", "nei", "nella", "o", "per", "qua'", "quello", "questo", "qui", "quindi", "quà", "sopra", "sotto", "su", "sul", "sulla", "tra", "un", "una", "uno"    ))

non_words = ("mm", "hmm", "ahm", "uhm", "ehm", "ah", "eh", "oh", "uh", "ih")


invalid_stop_words = ("c'è", "c'e'", "spa", "s.p.a.", "s.r.l.", "ecc", "etc") #TODO. Re-Check. not sure of what should go here
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

temporals = ("second", "minute", "hour", "day", "week", "month", "year", "decade", "century", "millennium", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "now", "yesterday", "tomorrow", "age", "time", "era", "epoch", "morning", "evening", "day", "night", "noon", "afternoon", "semester", "trimester", "quarter", "term", "winter", "spring", "summer", "fall", "autumn", "season", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
