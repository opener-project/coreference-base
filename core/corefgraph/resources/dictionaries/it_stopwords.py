# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'

#very basic stopword list.

stop_words = set(("﻿a", "ad", "ai", "al", "alla", "allo", "con", "cosi'", "così", "da", "del", "della", "dello", "dentro", "di", "e", "ecco", "ed", "fra", "fuori", "ha", "hai", "hanno", "ho", "il", "in", "nei", "nella", "o", "per", "qua'", "quello", "questo", "qui", "quindi", "quà", "sopra", "sotto", "su", "sul", "sulla", "tra", "un", "una", "uno"    )) 

extended_stop_words = set(("ad","ad"))

non_words = ("mm", "hmm", "ahm", "uhm", "ehm", "ah", "eh", "oh", "uh", "ih")


invalid_stop_words = ("c'è", "c'e'", "spa", "s.p.a.", "s.r.l.", "ecc", "etc") #TODO. Re-Check. not sure of what should go here
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

location_modifiers = ("east", "west", "north", "south", "eastern", "western", "northern", "southern", "upper", "lower")
