# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'

#very basic stopword list.

stop_words = set(("﻿a", "ad", "ai", "al", "alla", "allo", "con", "cosi'", "così", "da", "del", "della", "dello", "dentro", "di", "e", "ecco", "ed", "fra", "fuori", "ha", "hai", "hanno", "ho", "il", "in", "nei", "nella", "o", "per", "qua'", "quello", "questo", "qui", "quindi", "quà", "sopra", "sotto", "su", "sul", "sulla", "tra", "un", "una", "uno"    ))

non_words = ("mm", "hmm", "ahm", "uhm", "ehm", "ah", "eh", "oh", "uh", "ih")


invalid_stop_words = ("c'è", "c'e'", "spa", "s.p.a.", "s.r.l.", "ecc", "etc") #TODO. Re-Check. not sure of what should go here
invalid_start_words = ("'s",  "etc", )
invalid_end_words = ("etc", )

temporals = ("secondo", "secondi", "minuto", "minuti", "ora", "ore", "giorno", "giorni", "settimana", "settimane", "mese", "mesi", "anno", "anni", "decade", "decadi", "secolo", "secoli", "millennio", "millenni", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "sabati", "domenica", "domeniche", "adesso", "ieri", "domani", "dopodomani", "età", "tempo", "tempi", "periodo", "periodi", "era", "ere" , "epoca", "epoche", "mattino", "mattini", "mattine", "sera", "sere", "giornata", "giornate", "notte", "notti", "mezzogiorno", "mezzogiorni", "pomeriggio", "pomeriggi", "semestre", "semestri", "trimestre", "trimestri", "quadrimestre", "quadrimestri", "semestre", "semestri", "inverno", "inverni", "primavera", "primavere", "estate", "estati", "autunno", "autunni", "stagione", "stagioni", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre")
