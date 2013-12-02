# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi <valeria.quochi@ilc.cnr.it>'
__date__ = '5/13/13'


plural = ("noi", "voi", "loro", "essi", "esse", "ci", "ce", "vi", "ve", "li", "le", "nostro", "nostri","nostra","nostre", "vostro",  "vostri",  "vostra",  "vostre")

singular = ("io", "tu", "ti", "egli", "esso", "lui", "suo", "sua", "sue", "suoi", "ella", "essa", "lei", "sé", "lo", "la", "gli")

female = ("esse", "essa", "lei", "ella", "la", "le")
male = ("egli", "esso", "lui", "lo", "gli")
neutral = ("che", "cui", "quanto", "chi", "quando", "come", "quale", "quali")


animate = ("io", "me", "mi", "mio", "noi", "voi", "loro", "ci", "vi", "nostro", "nostra", "nostri", "nostre", "vostro", "vostra", "vostri", "vostre", "egli", "lui", "ella", "lei", "chi")

inanimate = ("esso", "essa", "quanto", "quando", "che", "come", "quale", "quali")

indefinite = set(("altro", "altra", "altri", "altre", "nessuno", "nessuna", "ciascuno", "ciascuna",
 "qualcuno", "qualcuna", "ognuno", "tutto", "tutti", "tutte", "tutta" "uno", "una", "molti", "molte", "molta", "nulla", "alcuni", "alcuno", "alcune", "alcuna", "certo", "certi", "certa", "certe", "diverso", "diversa", "diversi", "diverse", "parecchio", "parecchi", "parecchia", "parecchie", "tale", "tali", "troppo", "troppa", "troppi", "troppe", "poco", "poca", "pochi", "poche", "qualcosa", "niente", "tanto", "tanti", "tanta", "tante", "vario", "vari", "varia", "varie", "meno", "altrettanti", "piu'", "più", 
))


relative = ("che", "chi", "quale", "quali ", "dove", "cui", "quando")

reflexive = ("ja",)

no_organization = ("ja",)

third_person = ("ja",)

second_person = ("ja",)

first_person = ("ja",)

others = ("who", "whom", "whose", "where", "when", "which")

all = set(first_person + second_person + third_person + others)

pleonastic = ("it",)
